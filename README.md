# Generate PDF API

## Set up the project

1. Clone the project
2. Check the dependencies used in the ```libs.txt``` file. 
3. Rename the file ```.env.template``` to ```.env```
4. Set up the DataBase
```
docker-compose up -d
```
5. Run the ```app.py``` using the following command:
```
python app.py
```

## How to use the API

The API has the following endpoints:

```
GET    /
POST   /reports
GET    /reports
GET    /reports/:name
```

If you want to check the database connection, use:
```
GET /
```

To generate a report, use:
```
POST /reports
```
> [!NOTE]
> It is necessary to send ```name``` and ```paragraphs``` parameters in the request body.
> ```name``` refers to the report name and must be a string and unique
> ```paragraphs``` refers to the number of paragraphs you want in your text and must be a integer.

To see all generated report names, use:
```
GET /reports
```

To view a specific PDF report, use:
```
GET /reports/:name
```
> [!NOTE]
> ```:name``` refers to the report name.


________________________________

##Development Process

For solving this test, I began by identifying the problem and breaking it down into small steps.

Next, I identified the different libraries I would need and installed them.

Then, I started the Flask server and checked that everything was working correctly. Subsequently, I created the POST /generate-pdf endpoint as suggested in the document.

I visited the https://baconipsum.com/json-api/ page from which I would consume the information. After a few requests using Postman to better understand the API responses, I proceeded to integrate the request into the project using the requests library as recommended in the document.

I transformed the data from this request with the help of the pandas library to generate the DataFrame and NLTK for tokenization and data cleaning, in this case, removing punctuation and converting words to lowercase.

Then, I proceeded to analyze the information with the help of pandas and the implementation of some custom functions. Once the data was ready, I used Matplotlib to generate the respective graphs and finally generated the PDF with the help of the ReportLab library.

After completing this process, I created the docker-compose.yaml file to set up a MySQL database. With the help of the SQLAlchemy library, I made the necessary connections and stored the required information to generate the PDF. For this, it was necessary to create two additional endpoints to query the available reports and regenerate a PDF from any of them.

Finally, I drafted this document.
