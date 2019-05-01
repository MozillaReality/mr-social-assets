FROM node

# Install rust
ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH

RUN set -eux; \
    \
    # this "case" statement is generated via "update.sh"
    dpkgArch="$(dpkg --print-architecture)"; \
    case "${dpkgArch##*-}" in \
    amd64) rustArch='x86_64-unknown-linux-gnu'; rustupSha256='c9837990bce0faab4f6f52604311a19bb8d2cde989bea6a7b605c8e526db6f02' ;; \
    armhf) rustArch='armv7-unknown-linux-gnueabihf'; rustupSha256='297661e121048db3906f8c964999f765b4f6848632c0c2cfb6a1e93d99440732' ;; \
    arm64) rustArch='aarch64-unknown-linux-gnu'; rustupSha256='a68ac2d400409f485cb22756f0b3217b95449884e1ea6fd9b70522b3c0a929b2' ;; \
    i386) rustArch='i686-unknown-linux-gnu'; rustupSha256='27e6109c7b537b92a6c2d45ac941d959606ca26ec501d86085d651892a55d849' ;; \
    *) echo >&2 "unsupported architecture: ${dpkgArch}"; exit 1 ;; \
    esac; \
    \
    url="https://static.rust-lang.org/rustup/archive/1.11.0/${rustArch}/rustup-init"; \
    wget "$url"; \
    echo "${rustupSha256} *rustup-init" | sha256sum -c -; \
    chmod +x rustup-init; \
    ./rustup-init -y --no-modify-path --default-toolchain 1.25.0; \
    rm rustup-init; \
    chmod -R a+w $RUSTUP_HOME $CARGO_HOME;
# Install gltf_unlit_generator
RUN cargo install gltf_unlit_generator
# Install yarn
RUN curl -so- -L https://yarnpkg.com/install.sh | bash
# Prepare assets
RUN mkdir /assets
WORKDIR	/assets
COPY . /assets
RUN yarn install

# Copying things from the yarn setup script to generate a self signed certificate for the assets server. the hostname would be assets.mr.local
RUN mkdir certs; openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout ./certs/key.pem -out ./certs/cert.pem \
    -subj "/C=US/ST=State/L=Springfield/O=Dis/CN=assets.mr.local"
EXPOSE 8081
CMD yarn start
