# Full role prompts

Read [Solver](solver.md), [Critic](critic.md), [Refiner](refiner.md), and [answer extractor](answer_extractor.md) for formatted copies, or use [full_prompts.json](full_prompts.json) for the original template data. The JSON is byte-identical to the supplied prompt package; provenance and hashes are in [provenance.json](provenance.json).

| Role | Examples per request | Messages including system and current input |
|---|---:|---:|
| Solver | 8 | 18 |
| Critic | 2 | 6 |
| Refiner | 2 | 6 |
| Auxiliary answer extractor | 5 | 12 |

For a role call, the request contains its system instruction, all of that role's user/assistant examples in their saved order, and the current user input. These are reconstructed message arrangements from the templates, not captured HTTP request bodies. The extractor is an auxiliary answer-parsing role, not an additional refinement stage.

Both Critic examples continue refinement. Neither is a STOP example. The instruction requests the marker shown below when no improvement is needed:

````text
```STOP```
````

No new STOP/continue examples were added in this release, and the STOP analysis does not represent an experiment with a revised prompt. A low stopping frequency alone is not interpreted as low confidence. Source examples and generated answers are research artifacts; this release does not assign new rights to third-party content. See [data sources and attribution](../DATA_SOURCES.md).
