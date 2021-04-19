FROM python
RUN mkdir Harvestor
COPY . ./Harvestor/
RUN pip install -r ./Harvestor/requirements.txt
WORKDIR ./Harvestor/
CMD python app.py Twitter.txt
