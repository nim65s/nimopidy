FROM base/archlinux
RUN pacman -Syu --noconfirm python-pip npm
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -U -r requirements.txt
RUN npm install
RUN npm run build
