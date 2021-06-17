#buildah bud --layers --format docker -t kstych/resume-parser:latest .
#buildah tag #### kstych/resume-parser:latest
#buildah --format docker push kstych/resume-parser:latest

FROM fedora:latest
MAINTAINER kstych_private_limited

RUN dnf -y update
RUN dnf install python python-pip -y

RUN pip install -U pip setuptools wheel
RUN pip install spacy

RUN pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0.tar.gz

COPY ./kstych.sh /usr/local/kstych.sh

ENTRYPOINT ["/usr/local/kstych.sh"]
CMD ["/usr/local/kstych.sh"]


#podman run --rm -it --shm-size=2gb --name=py1 -v `pwd`/root:/root:Z -p 8080:8080 kstych/resume-parser:latest
