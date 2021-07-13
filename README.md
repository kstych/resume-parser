# resume-parser
SpaCy NLP and Reg-Ex based Resume Parser

# Build
use Buildah or docker to build the image

```buildah bud --layers --format docker -t kstych/resume-parser:latest .```

# Running

```podman run --rm -it --shm-size=2gb --name=resume-parser -v `pwd`/root:/root:Z -p 8080:8080 kstych/resume-parser:latest```

Now visit http://localhost:8080

