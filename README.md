# Application for maintaining a news feed - IT DIGEST ⚡
The application is quite simple, but the most functional in the area of working with content and search.
The application was originally developed on a standard sqlite database, and further migrations were made to the Postgresql server to use full-text search.
### Of the features:
  :white_check_mark: Sitemap and RSS feed  
  :white_check_mark: Comment System  
  :white_check_mark: Article tagging  
  :white_check_mark: Send your favorite article by email  
  :white_check_mark: Statistics calculation - for the latest and most commented articles  

### Last updates:
* Added article view counter, it increases by 1 every time the page is loaded. Redis was used.

### The ERD database diagram looks like this:
![Screenshot](https://github.com/DmitryZZZZZZ/Profiles/blob/master/media/images/ERD_pages.png)
### The main page displays a content block and a slidebar:
![Screenshot](https://github.com/DmitryZZZZZZ/Profiles/blob/master/media/images/main_page.jpg)
### Detail page:
![Screenshot](https://github.com/DmitryZZZZZZ/Profiles/blob/master/media/images/detail_page.jpg)
### A tagging system has been added to the block for displaying all articles:
![Screenshot](https://github.com/DmitryZZZZZZ/Profiles/blob/master/media/images/tag_system.jpg)
### Any user can write comments on the article:
![Screenshot](https://github.com/DmitryZZZZZZ/Profiles/blob/master/media/images/comments.jpg)
### Also, any user can send the article they like by e-mail to their friend:
![Screenshot](https://github.com/DmitryZZZZZZ/Profiles/blob/master/media/images/email.jpg)
### It is possible to subscribe to the RSS feed:
![Screenshot](https://github.com/DmitryZZZZZZ/Profiles/blob/master/media/images/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%2018.06.2023%20%D0%B2%C2%A013.37.jpeg)
