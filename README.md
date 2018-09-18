# UdacityProject_LogsAnalysis
This is a project based on the database provided by Udacity for full stack course, it is used to analyzed the data in the news database for completing the given tasks. You may find out the details from Udacity's webside.

For the reveiwers from Udacity, thank you for reviewing the project based on news database. This project includes three tasks:
- finding out the most three popular articles
- finding out the most popular author
- the days which error rate was higher than 1%


## Getting Started ##

### PreRequisites ###
- Python 2.7
- Vagrant
- VirtualBox

### setup ###
1. Install Vagrant and VirtualBox
2. Download or Clone fullstack-nanodegree-vm repository : https://github.com/udacity/fullstack-nanodegree-vm.
3. Download the news database from https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip.
4. Put 'newsdata.sql' into the vagrant directory which is shared with your virtual machine.
5. cd to vagrant directory and use the following command to launch the Vagrant VM:
	`$ vagrant up`
	`$ vagrant ssh`
6. cd into the vagrant directory and use the command following command to load the news database on your system
	`psql -d news -f newsdata.sql`
7. Now you have the news database, which includes articles, authors, log, please use `select * form table` to explore the three tables.


## Create views ##

There are two views created have to be created in the news database to run the code (news_report.py), wherein the first view is for the first and second tasks and the second view is for the last task. Please use the following code to create the views.


1. a view articles_details is created to include the log and authors information of articles:
	```
	create view articles_details as
	select articles.slug, log.path, log.id as log, authors.name, authors.id from articles
	left join log ON log.path LIKE CONCAT ('%',articles.slug)
	left join authors ON articles.author=authors.id
	```
	—notes: the table articles and authors do not have any column with the same content, but the column log.path includes a directory named by articles.slug, so CONCAT ('%',articles.slug) is used to join the two tables.-

2. view log_times is created to show the total number and error number of log on each days:

	```
  create view log_times as
	select * from
	(select CAST(time AS DATE) as total_date, count(*) as total_num
	from log group by CAST(time AS DATE)) as a
	left join
	(select CAST(time AS DATE) as error_date, count(*) as error_num
	from log where status!='200 OK' group by CAST(time AS DATE)) as b
	ON a.total_date=b.error_date;
	```
	—notes: two subquery are used,  first one used “count” and “group” to calculate the total number of logs on each day, and use CAST to take only date as the calculation unit, and the second one used the similar way to calculate the error logs on each days, wherein the logs which are not “200 OK” are regarded as error.-

## Run the code ##
After creating the views, you may use `python news_report.py` to run the news_report.py file and see the output of the three given tasks.
- The most three popular articles
- The most popular author
- The days with error rate higher than 1%

## Code Description ##
The code uses python2.7 / imports psycopg2 and datetime.

### The first task ###
In the python source code file, the sql query `select slug, count(*) as num from articles_details group by slug order by num desc limit 3` is used to select the slugs of the top three articles from the first view articles_details and put the result in result_ar, wherein —count- and —limit- are used to find out the top three articles with most logs (views).


### The second task ###
The sql query `select name, count(*) as num from articles_details group by name order by num desc limit 1;` to select the most popular author from the first view articles_details and put the result in result_au, wherein —count- and —limit- are used to find out the author with most logs (views).


### The third task ###
The sql query `select total_date as date,(error_num*100.0/total_num) as rate from log_times where (error_num*100.0/total_num) > 1;` to select the days with error rate higher than 1% from the second view log_times and put the result in result_er, wherein (error_num*100.0/total_num) is used to calculate the error rate percentage.

### Print ###
At the end, use python code to format the output and print the results of the three tasks.
