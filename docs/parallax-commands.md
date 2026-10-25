# Signed vehicle commands

These helpers extend the signed Parallax transport introduced in #229. Command
support depends on the vehicle's advertised features and software version.

`encode_frunk()`, `encode_windows()` and `encode_liftgate()` produce separate
closure-target messages for `body.closures.open` or `body.closures.close`.
The liftgate encoder selects only closure ID 7; it does not target the R1T tailgate.
`encode_control_command(command, params)` returns the RVM and protobuf payload
for cabin preconditioning, temperature, defrost, seat conditioning, steering-wheel
heat, charging start/stop, and charge limits. It accepts the existing
`VehicleCommand` parameter conventions. `CONTROL_COMMAND_FEATURES` identifies
the corresponding `PVS_COMF_CMD` or `PVS_ENRG_CMD` feature requirement.

Call `execute_command` with an enrolled phone identity, the vehicle public key,
and the enrolled phone private key. It subscribes to command state before sending
one command, then requires matching command ID and RVM plus successful terminal
status. It returns the command ID on confirmed success and raises
`ParallaxExecutionError` otherwise. Cancellation propagates to the caller and
subscription cleanup is attempted on every exit.

A transport error or timeout after submission leaves the outcome unknown. In R2
testing, charging operations sometimes changed vehicle state despite an operation
error with code 3. The helper preserves that error and warns that the command may
have taken effect. It does not retry, fall back to another transport, or infer
success from unrelated telemetry. Check current vehicle state before retrying.

Payload fields were checked against Android app 3.17.0. Physical testing covered
one R2: locks, frunk opening, cabin climate and temperature, driver-seat heat and
ventilation, steering-wheel heat, defrost, Gear Guard, and charging controls.
Charging worked in these tests, although some acknowledgements were inconsistent
as described above. No major charging-control problem was observed, but the cause
of those responses remains uncertain. Window commands did not move the windows;
the vehicle's iOS Shortcuts integration also reported window venting unavailable.
The R2 frunk closes manually, so powered frunk closing does not apply to this
vehicle. Rear liftgate and panic alarm have not been physically tested. Encoding support does not
establish vehicle support.
