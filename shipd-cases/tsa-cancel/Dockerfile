FROM public.ecr.aws/d3j8x8q7/olympus-base-rust:latest

USER root

ENV DEBIAN_FRONTEND=noninteractive \
    CARGO_INCREMENTAL=0 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    TZ=UTC \
    HOME=/home/model

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       ca-certificates \
       cmake \
       clang \
       libclang-dev \
       curl \
       git \
       libssl-dev \
       perl \
       pkg-config \
       python3-requests \
    && rm -rf /var/lib/apt/lists/*

RUN if ! id -u model >/dev/null 2>&1; then useradd --create-home --uid 1000 model; fi \
    && mkdir -p /app /home/model/.cargo \
    && chown -R model:model /app /home/model

# test.sh may run under a UID that has no /etc/passwd entry (the verifier's
# runtime user differs from the "model" UID used to build this image).
# crates/integration-tests/src/kumod.rs resolves the current UID to a
# username via NSS before spawning kumod and fails with "couldn't resolve
# myself" when that lookup is empty. Make /etc/passwd writable so the
# runtime user can add itself; test.sh performs the actual self-heal.
RUN chmod 666 /etc/passwd

WORKDIR /app
COPY --chown=model:model . .

# The upstream .dockerignore excludes docs/, but solution.patch updates the
# checked-in TSA OpenAPI snapshot. Restore its exact pinned-commit baseline so
# the patch can be applied inside the verifier image.
RUN mkdir -p docs/reference \
    && curl --fail --silent --show-error --location \
       https://raw.githubusercontent.com/KumoCorp/kumomta/2a40536127e243065dbaa64f616f386eeb1a91db/docs/reference/tsa-daemon.openapi.json \
       --output docs/reference/tsa-daemon.openapi.json \
    && chown -R model:model docs

USER model

RUN cargo fetch --locked && cargo build --locked -j 5 -p kumod -p tsa-daemon -p kcli && cargo test --locked -j 5 -p integration-tests test::tsa_basic_automation::tsa_basic_automation --no-run

# test.sh's flock-wrapped commands may execute as a UID other than the one
# that built this image (e.g. the verifier's own runtime user). Cargo needs
# to rewrite fingerprints, remove stale artifacts, and take its own internal
# lock (target/debug/.cargo-lock) under target/, so make the whole tree
# writable by any UID rather than just the build-time owner.
RUN chmod -R a+rwX target

ENV CARGO_NET_OFFLINE=true
CMD ["/bin/bash"]
