# Diagnostic lessons; campaign INCONCLUSIVE

Scope: [acceptance issue #10](https://github.com/ThinkFlowLab/OmniRSI/issues/10).
The user-confirmed bounds and frozen validator remain unchanged. All baseline
quality repetitions are now complete. No candidate has passed the required
all-concurrency performance and quality matrix, so no successful README example
is added.

The [published runtime evidence](https://github.com/david6666666/drama-3-single-b300-inference/tree/2669d4cc67f2c3db29f8c10167f26a447a877bdd/evidence/20261015-scale150)
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
