/** Copyright 2020 Alibaba Group Holding Limited.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

#ifndef EXAMPLES_ANALYTICAL_APPS_PAGERANK_PAGERANK_CONTEXT_H_
#define EXAMPLES_ANALYTICAL_APPS_PAGERANK_PAGERANK_CONTEXT_H_

#include <iomanip>

#include <grape/grape.h>

namespace grape {
/**
 * @brief Context for the batch version of PageRank.
 *
 * @tparam FRAG_T
 */
template <typename FRAG_T>
class PageRankContext : public VertexDataContext<FRAG_T, double> {
  using oid_t = typename FRAG_T::oid_t;
  using vid_t = typename FRAG_T::vid_t;

 public:
  explicit PageRankContext(const FRAG_T& fragment)
      : VertexDataContext<FRAG_T, double>(fragment, true),
        result(this->data()) {
    auto inner_vertices = fragment.InnerVertices();
    auto vertices = fragment.Vertices();
    degree.Init(inner_vertices);
    next_result.Init(vertices);
    avg_degree = static_cast<double>(fragment.GetEdgeNum()) /
                 static_cast<double>(fragment.GetInnerVerticesNum());

    send_buffers.resize(fragment.fnum());
    recv_buffers.resize(fragment.fnum());
    for (fid_t k = 0; k < fragment.fnum(); k++) {
      size_t send_size = fragment.MirrorVertices(k).size() * sizeof(double);
      size_t recv_size = fragment.OuterVertices(k).size() * sizeof(double);
      send_buffers[k].resize(send_size);
      memset(send_buffers[k].data(), 0, send_size);
      recv_buffers[k].resize(recv_size);
      memset(recv_buffers[k].data(), 0, recv_size);
    }

#ifdef PROFILING
    preprocess_time = 0;
    exec_time = 0;
    postprocess_time = 0;
#endif
  }
  ~PageRankContext() {}

  void Init(BatchShuffleMessageManager& messages, double delta, int max_round) {
    this->delta = delta;
    this->max_round = max_round;
    for (fid_t i = 0; i < this->fragment().fnum(); i++) {
      messages.SetupBuffer(i, std::move(send_buffers[i]),
                           std::move(recv_buffers[i]));
    }
    step = 0;
  }

  void Output(std::ostream& os) override {
    auto& frag = this->fragment();
    auto inner_vertices = frag.InnerVertices();
    for (auto v : inner_vertices) {
      os << frag.GetId(v) << " " << std::scientific << std::setprecision(15)
         << result[v] << std::endl;
    }
#ifdef PROFILING
    VLOG(2) << "preprocess_time: " << preprocess_time << "s.";
    VLOG(2) << "exec_time: " << exec_time << "s.";
    VLOG(2) << "postprocess_time: " << postprocess_time << "s.";
#endif
  }

  typename FRAG_T::template inner_vertex_array_t<int> degree;
  typename FRAG_T::template vertex_array_t<double>& result;
  typename FRAG_T::template vertex_array_t<double> next_result;
  std::vector<std::vector<char, Allocator<char>>> send_buffers;
  std::vector<std::vector<char, Allocator<char>>> recv_buffers;

#ifdef PROFILING
  double preprocess_time = 0;
  double exec_time = 0;
  double postprocess_time = 0;
#endif

  vid_t total_dangling_vnum = 0;
  vid_t graph_vnum;
  int step = 0;
  int max_round = 0;
  double delta = 0;

  double dangling_sum = 0.0;
  double avg_degree = 0;
};
}  // namespace grape

#endif  // EXAMPLES_ANALYTICAL_APPS_PAGERANK_PAGERANK_CONTEXT_H_
