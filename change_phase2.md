
<!-- Changes that should be applied in the second phase -->

# we should only have a priority tag named URGENT and another one for high

    - fields should be changed on the database. the default value when a ticket is created is high
    - there should be a radio button named urgent on the template ( add it as an input button with type radio button)

# stars for ticket quality should be numeric on a scale of 5 

    - the field can still be integerfield 
    - a template div should be found to represented instead of a multiple choice.

# the urgent option for priority in tickets should be displayed as a radio button when creating a ticket

    - after adding an URGENT value to the priority name field, change the related view 
    - create a input radio button for the urgent option

# calls are banned . the panel should have voice mails for interorganizational communications

    - the only thing needed to add is to write a label for the interorganizational voice mail

# when someone is a member in two organizations there should appear as tabs for the organization ticket section (as a dropdown)

    - the session issue is to be fixed
    - ROLES should be defined : (this may involve views,model and a section for the admin to control everything !)

# There should be an All ticket section that only the CEO can monitor

    - After defining roles ...
        - Add a sidebar option dropdown for the ALL TICKETS
        - Create a template for the ALL_TICKET section
        - write a view for it
        - modify the django template

# ticket quality assessment should only be open for the CEO

    - After dealing with session issue ...
    - After defining the ROLES ...
    - set the user to only see ticketquality section
    - find a way to only display the sidebar ticketquality option for the CEO 

# A department can't issue a ticket for a customer unless that person is defined as a customer in the database.

    - add a validation to the view relevant to ticket creation to check whether the customer exists in the database 

# in the ticket creation section : add one more field for a phone number. either mobile2 or home.

    - change the model, add a second number field to the database
    - change the forms.py 
    - add a field to the ticket creation for second phone number

# remove insta and linkedin icons

    - remove the insta and the linkedin sections from the template/partials

# the ordering of the tickets in each segment should be based on the last change occuring on that ticket.

    - Add an updated/modified_at field to tickets both in the models and database
    - Set it so that null is acceptable ( because tickets dont have any value for that option)
    - the changes that cause this updated at should be researched

# potential changes that could lead to updating a ticket to the top of the list are as follows:

    - any form field that gets updated in the viewTicket section will change the updated_at field in the database for the object

# Fix the issue of Users : the users model in the models.py should be a superset of the django model

    - search this problem

* Note : there is a problem now with the sales department. Sometimes they dont know whether they have sent a ticket or not. 
* there should be an option for an organization based on its need to be able to see  the tickets sent by its memebers.

###############################################