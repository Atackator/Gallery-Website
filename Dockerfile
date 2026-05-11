FROM python:3.9-alpine
WORKDIR /iap1-tema
COPY . /iap1-tema
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
ENV NAME PhotoGallery
CMD ["python", "app.py"]
