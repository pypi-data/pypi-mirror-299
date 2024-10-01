# Copyright (c) 2021 Mobvoi Inc. (authors: Binbin Zhang)
#               2023 Tsinghua Univ. (authors: Xingchen Song)
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List
from collections import defaultdict

import torch

from .context_graph import ContextGraph
from .prefix_score import PrefixScore
from .utils import log_add


def ctc_greedy_search(
    ctc_probs: torch.tensor,
    ctc_lens: torch.tensor,
    blank_id: int = 0,
):
    results = ctc_prefix_beam_search(ctc_probs, ctc_lens, 1, blank_id=blank_id)
    return {
        "best": results["nbest"][0],
        "scores": results["nbest_scores"][0],
        "times": results["nbest_times"][0],
    }


def ctc_prefix_beam_search(
    ctc_probs: torch.tensor,
    ctc_lens: torch.tensor,
    beam_size: int,
    context_graph: ContextGraph = None,
    blank_id: int = 0,
):
    results = []
    # CTC prefix beam search can not be paralleled, so search one by one
    for ctc_prob, num_t in zip(ctc_probs, ctc_lens):
        context_state = None if context_graph is None else context_graph.root
        cur_hyps = [(tuple(), PrefixScore(s=0.0, v_s=0.0, context_state=context_state))]
        # 2. CTC beam search step by step
        for t, logp in enumerate(ctc_prob):
            # key: prefix, value: PrefixScore
            next_hyps = defaultdict(lambda: PrefixScore())
            # 2.1 First beam prune: select topk best
            logp, indices = logp.topk(beam_size)  # (beam_size,)
            for prob, u in zip(logp.tolist(), indices.tolist()):
                for prefix, prefix_score in cur_hyps:
                    last = prefix[-1] if len(prefix) > 0 else None
                    if u == blank_id:  # blank
                        next_score = next_hyps[prefix]
                        next_score.s = log_add(
                            next_score.s, prefix_score.score() + prob
                        )
                        next_score.v_s = prefix_score.viterbi_score() + prob
                        next_score.times_s = prefix_score.times().copy()
                        # perfix not changed, copy the context from prefix
                        if context_graph and not next_score.has_context:
                            next_score.copy_context(prefix_score)
                            next_score.has_context = True
                    elif u == last:
                        # Update *uu -> *u;
                        next_score1 = next_hyps[prefix]
                        next_score1.ns = log_add(next_score1.ns, prefix_score.ns + prob)
                        if next_score1.v_ns < prefix_score.v_ns + prob:
                            next_score1.v_ns = prefix_score.v_ns + prob
                            if next_score1.cur_token_prob < prob:
                                next_score1.cur_token_prob = prob
                                next_score1.times_ns = prefix_score.times_ns.copy()
                                next_score1.times_ns[-1] = t
                        if context_graph and not next_score1.has_context:
                            next_score1.copy_context(prefix_score)
                            next_score1.has_context = True
                        # Update *u-u -> *uu, - is for blank
                        n_prefix = prefix + (u,)
                        next_score2 = next_hyps[n_prefix]
                        next_score2.ns = log_add(next_score2.ns, prefix_score.s + prob)
                        if next_score2.v_ns < prefix_score.v_s + prob:
                            next_score2.v_ns = prefix_score.v_s + prob
                            next_score2.cur_token_prob = prob
                            next_score2.times_ns = prefix_score.times_s.copy()
                            next_score2.times_ns.append(t)
                        if context_graph and not next_score2.has_context:
                            next_score2.update_context(context_graph, prefix_score, u)
                            next_score2.has_context = True
                    else:
                        n_prefix = prefix + (u,)
                        next_score = next_hyps[n_prefix]
                        next_score.ns = log_add(
                            next_score.ns, prefix_score.score() + prob
                        )
                        if next_score.v_ns < prefix_score.viterbi_score() + prob:
                            next_score.v_ns = prefix_score.viterbi_score() + prob
                            next_score.cur_token_prob = prob
                            next_score.times_ns = prefix_score.times().copy()
                            next_score.times_ns.append(t)
                        if context_graph and not next_score.has_context:
                            next_score.update_context(context_graph, prefix_score, u)
                            next_score.has_context = True

            # 2.2 Second beam prune
            next_hyps = sorted(
                next_hyps.items(), key=lambda x: x[1].total_score(), reverse=True
            )
            cur_hyps = next_hyps[:beam_size]

        # We should backoff the context score/state when the context is
        # not fully matched at the last time.
        if context_graph is not None:
            for i, hyp in enumerate(cur_hyps):
                context_score, new_context_state = context_graph.finalize(
                    hyp[1].context_state
                )
                cur_hyps[i][1].context_score = context_score
                cur_hyps[i][1].context_state = new_context_state

        results.append(
            {
                "nbest": [list(y[0]) for y in cur_hyps],
                "nbest_scores": [y[1].total_score() for y in cur_hyps],
                "nbest_times": [y[1].times() for y in cur_hyps],
            }
        )
    return results
