# Diagnostic lessons; campaign INCONCLUSIVE

Scope: [acceptance issue #10](https://github.com/ThinkFlowLab/OmniRSI/issues/10).
The user-confirmed bounds and frozen validator remain unchanged. All baseline
quality repetitions are now complete. No candidate has passed the required
all-concurrency performance and quality matrix, so no successful README example
is added.

The [published runtime evidence](https://github.com/david6666666/drama-3-single-b300-inference/tree/e58c8418005af8972d1616d5368009bc07dbe651/evidence/20261015-scale150)
retains the following useful failures and controls:

- Compare actual batch sizes when attributing decode kernels. Mixed-batch
  averages and a full-batch diagnostic cannot establish a kernel regression.
  When streams overlap, summed kernel durations exceed elapsed graph time.
- A whole-network single/batch parity failure needs an unchanged control.
  Both packed and unchanged padded prefill exceeded the initial whole-network
  error bound. That failure remains recorded. A separately declared experiment
  compared each operator on identical real layer inputs and retained its
  numeric threshold, graph/eager parity and exact ownership checks.
- State ownership checks must include real rows, dummy primary rows and GDN
  suffix scratch rows. Snapshot unrelated state before CUDA Graph replay;
  checking only eager execution misses replay-specific writes. Invalid test
  setup failures are retained separately from runtime failures.
- Removing an existing atomic prefill reduction resolved the tested packed
  graph/eager mismatch. Experimental packed serving uses ordered reduction;
  this observation does not establish bitwise equivalence for every model path.
- Fused tower projections improved a real decode microbenchmark but did not
  improve the full service trial. Multi-step decode passed exact state/output
  checks but delayed admission and did not improve service throughput. Neither
  is selected on its kernel result alone.
- Concurrent prefill/decode preserved tested states on an isolated GPU, but the
  diagnostic excludes first-frame sampling, scheduling and codec. Its timing
  cannot be promoted as service throughput. An earlier timing on a device with
  an observed external worker is explicitly unqualified.

Complete quality from an individual feasible configuration is useful evidence,
but it does not fill missing concurrency or repetition groups. The imported
catalog guidance remains `locally_verified=false`; these observations do not
automatically qualify another engine, revision, GPU or workload.

The user confirmed that further optimization must retain native computation,
all eight routed experts, and no additional lossy quantization. Historical
precision-reduction trials remain rejected; frozen acceptance gates are intact.

New fixed-request controls cover complete generated codes, model/codec state,
PCM bytes, completion ordering and two generations of slot reuse. Decode/codec
and prefill/codec concurrency both preserve the tested outputs exactly. Yet
fresh asynchronous service trials fail complete WER in both the unchanged
control and the fused-input candidate. These failures remain in the runtime
evidence and the async configuration is not selected. Do not infer a CUDA race,
a successful fix, or acceptable dynamic-service quality from those replay
controls alone. No root cause has been established.

Nonblocking CUDA events also show substantial existing codec/decode overlap.
Exclude warmup using the raw request interval, distinguish submission from
codec execution, and do not count overlapped time twice as an available gain.
Event spans can contain submission gaps and do not measure SM utilization.

The new native MoE input preparation preserves every FP8 activation byte,
scale and router value, and complete B16/B64 replay state. This numerical result
is separate from serving acceptance, which remains incomplete.

A separate native-fusion pair with synchronous codec subsequently completed on
the frozen physical GPU0. All 1088 outputs in each arm meet the issue's quality
bounds, but throughput still misses the updated baseline and acceptance target.
This is one feasibility repetition, not a qualified all-concurrency result.
The successful fixed-input fusion and this limited service observation do not
promote the rejected asynchronous configuration or resolve its failure cause.
