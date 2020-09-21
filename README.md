# companies-registry-parser
Test task for Schwarzthal Tech

## Task description
1) Write a parser for Dubai International Financial Centre public registry: https://www.difc.ae/public-register/. 
2) Put parsed data in any database (MongoDB is strongly recommended)

## Occured problem and its solution
The only problem was "infinitely" scrolling page. Using browser network console I found links that dynamically came during the scrolling. All of them had the same structure:

* https://www.difc.ae/public-register/?companyName=&registrationNo=&status=&type=&sortBy=&page=NUMBER&isAjax=true, where NUMBER ranges from 1 to 406.
  
Each of this page stores information about approximately ten companies with the link to their profile views. Based on this information I implemented two solutions for the task. 

## My parsing solution
I divided my solution into two parts: basic and advanced parsers. Both they retrieves necessary information about companies. However, advanced parser extracts more significant fields such as directories and date of incorporation.

* Basic parser. Takes the information only from pages that dinamically came while scrolling. Works fast because has depth equal to zero. Retrieves the next fields:
  * Company name
  * Location
  * Status of registration (active or not)
  * Registred number
  * License number

* Advanced parser. Takes the information from the profile view extracting the left bottom table "Company information". Works very slow because of crawling companies view pages. Retrieves the next fields:
  * Company name
  * Trading name
  * Status of registration 
  * Type of License
  * Type of Entity
  * Date of Incorporation
  * Commercial License Validity Date
  * Directors
  * Shareholders
  * DNFBP
  * Financial Year End
  * Class of Issued Shares
  * Number of Issued Shares

There are totally 4056 companies in the public register as seemed after the parsing.

### Database
* I have chosen MongoDB for the database and load the data from parser into MongoDB cluster. As you can see below the cluster stores a database with 4056 records about companies in "Companies" collection.

![](https://i.imgur.com/3cQKP8k.png)

![](https://i.imgur.com/15umvfE.png)

* Another screen proofing that database stores data retriveing from parser:

![](https://i.imgur.com/SNLgiBs.png)
