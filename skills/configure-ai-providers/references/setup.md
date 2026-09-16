# Local service qualification

Use [provider setup](PROVIDERS.md) for environment files, routes, and runnable checks.

Before a generation batch, record the target service's actual model/node inventory, GPU identities, memory budgets, managed limits, and current queue. Device numbering can differ by backend. Preserve unrelated workloads and select smaller validated jobs when resources are limited.

For remote services use your own authorized HTTPS endpoint or authenticated loopback tunnel. Loopback always means the machine executing the helper; a container or remote coding environment may need a different address. This package contains no machine access profile.

A successful status request establishes connectivity only. Qualify one still and one short clip on that exact installation, and inspect the result. Changing the GPU, runtime, model, adapter, or graph can change quality, memory needs, and timing.
