
# BoutiqueAdo

- This website is not published but if you would like to navigate it, speak with Gaberoids (Gabriel). Meanwhile enjoy the pictures and descriptions of this website.


## Author
Gabriel Perguer Figueiro


## Project Overview
 
- This website is designed to be an online store for multiple types of merchandise such as clothing and house a items.

### Strategy
- To make the website visually appealing to customer.
- To provide the the customer a toll that will allow him to perform all necessary activities for him to shop remotely.

## UX
- The user experiece focus is to provide to the customer a tool that is so intuitive that even a not educated adult will be able to use it without assistence of other person or user guide.

### Scope
The scope of this project includes 
- To provide information necessary for the customer to an educated purchase.
- To provide the features for the customer to place and manage current and past orders.
- To provide administrative functionality for online store owners and administrators.
- At this stage, the capacity to cancel an existig order and to track the order progress is ot available but it may be part of future enhencements.
- At this stage, there is no review system but it may be part of future enhencements.

### Project Goals
- To display web developer skills.

### Developer Goals
- To produce a website that will be easy to navigate 
- To produce a website that will be easy to read. It should be informative but using the least amount of words possible.
- Interactive tool. The pages will respond to users actions such as mouse hoovering or clicking buttons.

### Users Analysis
1- Who this website is for?  
Answer: This website is for people interested in buying items online and have those items delivered to addresses of their choices.

2- What it is that users want to achieve with this website?  
Answer: To make educated purchase of online items and to have those items delivered to addresses of their choices. 

3- How your project is the best way to help them achieve these things?  
Answer: The website website will be informative and intuitive.

#### User Goals
> - New users:
- They want to find the items they are looking for.
- The want information about the items they are interested in buying.
- They want to buy the item online and receive it in their homes.
- They want to create an profile to have the ability make future purchases easier (Ex: to save billing address in profile. This way customer does not have to enter this info again in order to place future orders).


> - Returning users:
- They want to be able to see their order history.
- They want the buy more items

> - System Administrators:
- They want manage inventory available on for purchase online (add or remove items from the store).
- They want manage users access and restrictions on the website.


__User Stories:__   
  
| User Action        | Goal          |
| ------------- |:-------------:| 
| User enters key words to the search box   | to find items related to key words from search box| 
| User selects multiple items     | Buy multiple items to enjoy free shipping benefits       |  
| Adminitrators add and remove items available online | to keep inventory online updated      |
| Adminitrators check on list of orders  | To know what items need to be shipped     |

## Design Choices

### Colors
- Base colors
  - Mostly Neutral colors such as white black, tones of gray.
- Bright colors will be used by the system to draw customer attention to the parts of the site that are more relevant to the customer when it comes to purchasing an item.

### Typography (???):
  - Font style:
    - The are meant to make the site to look fancy. 
      - Tittle and subtitle font family: Lato
      - ![Fonts_Tittle_subtittle](https://fonts.google.com/specimen/Lato)

  - Font size: 
    - Bigger letters are meant to draw the users attention. Also, they are meant to give the users an idea of what the content attached to them is about.
    - The font size become smaller as the text informative purpose increases. The more informative is , more wordy the text gets.    

### Design Elements
Elements used in this website:
- top menu (desktop navigation)
- Hamburger icon menu (mobile navigation)
- containers
- button html tag
- text input
- textarea HTML element
- images
- tooltips
- icons
- contact form
- Others: div, paragraphs, head, title, script, body, link (<a>), header, headings, unordered list, label, section, html, figure, meta.

### Images
Images are used to show the products for sale.
Icons are used sometimes to substitute text when texts occuppy too much space on the page. Also, when the icon meaning is obvious to reasonable people.
  


## Features
 
- ### Existing Features
    - Clickable buttons and links
    - Form Contact Us page
    - Photo gallery with zoom capability
    - Navigation bar. Hamburger icon on mobile version 
    - Send a message to genealogy consultant
    - Email validation on contact us page
    - Responsive Grid system
    - Website supported by jasmine tests
    - Icons and background image

- ### Features Left to Implement
    - To improve navigation bar style
    - Ability to search in the web filtered by location.
    - Improve the way images are displayed when they are zoomed in (index.html).
    - Ability for users to visit consultant's social media and share the site.
    - Consultant reviews ( 3 reviews).

## Technologies Used

[Bootstrap](https://getbootstrap.com/docs/4.0/utilities/display/) 
    - The navigation bar (in all pages), the photo gallery (Questions section) portions of the index.html, and contact us portion of contact.html page were built with a template from **bootstrap** to speed up development. However, the templates have been modified from its original for customization purposes.   

[Google Fonts](https://fonts.google.com/)
    - **Google Fonts** was used to style the fonts of the project.

[Viewport](https://www.w3schools.com/css/css_rwd_viewport.asp) 
    - Meta name **viewport** was also added in order to make the site responsive to different sizes of screen.

[Javascript](https://www.javascript.com/)
    - This technology was used to link APIs to the website (Google Search and Emailjs APIs)

[Jquery](https://jquery.com/)
    - This library was used to create an interactive User Interface (Zoom functionality found on the index.html "questions" sections)

[Jasmine](https://en.wikipedia.org/wiki/Jasmine_(JavaScript_testing_framework))
    - This framework was used to test javascript code, such as the code that validate the email input text box found in the contact.html page 



## Testing

Automated tests
1. Email validation
    - Go to https://gaberoids.github.io/genealogynow/assets/readme_files/tests.html to see test results.
    - The link to the test file: https://github.com/Gaberoids/genealogynow/blob/master/assets/spec/calcSpecs.js .
    - The link to the page where the function being tested is found: https://github.com/Gaberoids/genealogynow/blob/master/assets/js/calc.js .

Non-automated tests
1. Navigation bar:
    1. Go to the "Homapage" page
    2. Click on all links and buttons to see if they work and take the user to the pages they meant to go.
    3. Change the size of the screen to make sure that the navbar is presentable
    4. Click the links and button again in different size of screens to verify they still work (mainly when hamburger icon shows).

2. "Questions" section of the homepage:
    1. Go to the "Home" page (index.html)
    2. Hover over the small pictures on the right side of the page and note the cursor turn into a magnifying glass.
    3. Click the small pics and notice that they exchange position with with the pic placed on the big frame.  
    4. Change sizes of the screens to make sure that the site is still presentable and functional on those sizes.

3. Search functionality:
    1. Go to the "geniusSearch.html" page and type "Perger" inside the search box.
    2. Note how the search returns many results.
    3. Note that the search results are related to the key words "Perger" (typed by the user) plus "family" and "genealogy" (default key words).
    4. Make sure the content of the page is presentable in all sizes of screen.
    5. Make sure that the text box are working with all sizes of the screen by typing text in them and hitting enter.

3. Contact us functionality (Mandatory fields, email validation, send email):
    1. Go to "https://gaberoids.github.io/genealogynow/contact.html" .
    2. Without typing anything click "Submit Inquiry".
    3. Note alert a click ok.
    4. Type something in the text box for email and submit.
    5. Click ok and delete the email text.
    6. Type something in the message and submit.
    7. Click ok and add an email address to the email input box and submit. This time, you should get a message that confirms that an email has been sent out.
    8. To confirm that the email was sent go to gmail.com, log in into gmail.com with the following credentials:
        - User name: geniusgenealogy@gmail.com
        - Password: codeacademyadmin
    9. Note that an email was received from the website contact page.

    (*CLARIFICATION NOTE: Testing screen size means -> by increasing and decreasing the browser window and using developer tools to test site on mobile view.*)


**The pages in this website will be more simple in the mobile view compared to desktop view. For example:**
- links in the menu navigator will be replaced by the hamburger icon.
- In the index.html, the head shot from consultant will be removed on mobile screen.

**Bugs:**  
- There is an error message on index.html. It says "Uncaught TypeError: Cannot read property 'step' of undefined.". According to my research, this error has to do with Jquery CDNs. This bug is not breaking the page right now, so I left it alone for now.

## Deployment

Link to the github repository https://github.com/Gaberoids/genealogynow .

Link to the deployed site https://gaberoids.github.io/genealogynow/ .

Deplyed and development versions have no differences.

**Deployment steps:**
1. Go to the link https://github.com/Gaberoids/genealogynow .
2. Click the tab "Settings".
3. Under the section "HUB Pages" click the drop down button under "Source" and select "Master Branch".
4. Go to under the "HUB Pages" section again, and click on the link. This link is the address to the deployed site.

**Cloning Repository steps:**
1. Go to the link https://github.com/Gaberoids/genealogynow .
2. Click the green button "Code".
3. Select the option "Download Zip".
(For more information on how to clone the repository, visit https://docs.github.com/en/enterprise/2.13/user/articles/cloning-a-repository)


## Credits
- My tutor at code academy Moosa. He helped me with directions on how to how to improve the visual presentation of the site and helped me with some the jasmine test.
- Special thanks to [TMS Tree icon by Icons8](https://icons8.com/icon/34828/tms-tree) for providing the cool logo for this website.

### Content
- The content of this website is original.

### Media - Source of all pictures that are not original
* #### Index.html page
    * ##### Cover
        - [cover-tree.jpg](https://www.freeimages.com/photo/trees-1393133)
    * ##### Question Section
        * ###### How they look like?
            -  [old-headshot.jpg](https://www.freeimages.com/photo/old-framed-picture-1433232)
            -  [old-photos-multiple.jpg](https://www.freeimages.com/photo/old-photos-1434448)
            -  [old-family-bench](https://www.freeimages.com/photo/old-family-photo-2-1433934)
            -  [old-family-portrait](https://www.freeimages.com/photo/old-time-family-photo-1311342)
        * ###### Where they came from?
            -  [where_castle.jpg](https://www.freeimages.com/photo/irish-abbey-1214069)
            -  [where_africa.jpg](https://www.freeimages.com/photo/africa-1406054)
            -  [where_india.jpg](https://www.freeimages.com/photo/taj-1307962)
            -  [where_china.jpg](https://www.freeimages.com/photo/theatre-stage-1235519)
        * ###### How they came from?
            -  [how-wagon.jpg](https://unsplash.com/photos/QFhIVlX9wTs)
            -  [how-ship.jpg](https://www.freeimages.com/photo/sailing-ship-in-harbor-1450308)
            -  [how-train.jpg](https://www.freeimages.com/photo/steam-locomotive-1447997)
            -  [how-car.jpg](https://www.freeimages.com/photo/my-granny-in-old-car-1440617)

* ### Contact.html page
    -  [contact-tree.jpg](https://www.freeimages.com/photo/tree-on-the-hill-1385676)

* ### Search.html page
    -  [search-bk-image.jpg](https://www.freeimages.com/photo/old-family-photos-1423774)

### Acknowledgements

I received inspiration for this project from [Codeacademy](https://courses.codeinstitute.net/).
- The modal functionality and the Mobil hemburger buttons were built inspired on templates from bootstrap.
 

