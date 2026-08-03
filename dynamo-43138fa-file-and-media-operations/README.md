# Willow Manifest Recovery

This Harbor task asks the agent to recover `/app/release_manifest.json` from a failed tar-based release export at `/app/data/willow_drop.tar`.

The task focuses on file permissions and metadata. A correct solution must replay the tar stream as a virtual filesystem, ignore unsafe paths, apply tombstone delete markers, resolve hardlinks at the moment they appear, preserve symlink targets, honor PAX paths, apply byte overlays from `meta/overlays.tsv`, and apply the out-of-order permission ledger stored in `meta/permissions.tsv`.

The environment uses the approved pinned Ubuntu base image and builds the deterministic recovery capsule during image build. The verifier runs with dependencies baked into the shared image, pins the input archive SHA-256, rejects missing/empty/symlinked outputs, validates the JSON schema, and compares all final manifest records against independent expected values in `task/tests/test_outputs.py`.
