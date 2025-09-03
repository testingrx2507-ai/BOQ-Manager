# BOQ Manager App for ERPNext

Hi! This is my first ERPNext app that I made for managing Bills of Quantities (BOQ). I'm still learning but I think it turned out pretty good!

## What This App Does

So basically, I created this app because I needed to handle BOQs in ERPNext. A BOQ is like a list of items and quantities you need for a project (I learned this during the assignment lol).

The app lets you:
- Create BOQ documents with items and quantities 
- Make quotations from the BOQ automatically
- Create projects and tasks from the BOQ
- See reports of everything connected

## How I Built It

### Day 1 - Making the Basic Stuff

First I had to create a new app using the bench command:
```
bench new-app boq_manager
bench --site [site-name] install-app boq_manager
```

Then I made two DocTypes using the GUI (much easier than coding!):

**1. Bill of Quantities**
- title: what the BOQ is called
- customer: who it's for  
- boq_date: when you made it
- total_amount: adds up all the money (this was tricky!)
- status: Draft/Submitted/Quoted
- boq_items: table of all the items

**2. BOQ Item** (child table)
- item_code: links to ERPNext items
- item_name: gets filled automatically (cool!)
- description: what the item is
- quantity: how many you need
- rate: price per item
- amount: quantity × rate (calculated automatically)
- uom: unit like kg, pieces, etc.

### The Hard Part - Making Calculations Work

I had to write Python code to make the totals calculate automatically. This was really confusing at first but I figured it out:

```python
def calculate_total_amount(self):
    total = 0
    for item in self.boq_items:
        if item.quantity and item.rate:
            item.amount = item.quantity * item.rate
            total += item.amount
    self.total_amount = total
```

I also had to add this to hooks.py so it runs automatically when you save the BOQ. Took me a while to understand what hooks are!

### Day 2 - Connecting Everything Together  

This was the really hard part. I had to make the BOQ connect to Quotations, Sales Orders, and Projects.

**Adding Custom Fields**
I learned you can add fields to existing DocTypes! I added:
- boq_reference field to Quotation
- boq_reference field to Sales Order  
- boq_reference field to Project
- boq_quantity_needed field to Task

**Making Buttons Work**
I added buttons using Client Script (JavaScript is scary but I managed):
- "Create Quotation" button on BOQ
- "Create Project" button on BOQ

**The Python Functions**
These were the hardest part! I had to write functions that create new documents:

`create_quotation_from_boq()` - takes all the BOQ items and makes a quotation
`create_project_from_boq()` - makes a project and creates tasks for each item

I had to use `@frappe.whitelist()` to make them work from the buttons (learned this the hard way after getting errors!).

## Problems I Had and How I Fixed Them

**Problem 1**: Total amount wasn't calculating
- **Solution**: Had to use hooks.py and the validate method

**Problem 2**: Buttons weren't showing  
- **Solution**: Client Script needed the right docstatus check

**Problem 3**: Getting "AttributeError: no attribute 'boq_items'"
- **Solution**: Child table fieldname didn't match what I put in the code

**Problem 4**: Status field showing "Draft<br>Submitted<br>Quoted"
- **Solution**: Had to put each option on a new line in the DocType

## The Report I Made

I created a Query Report that shows everything connected:
- BOQ Name
- Customer  
- Quotation (if made)
- Sales Order (if made)
- Project (if made)

The SQL was hard to write but I used JOINs to connect all the tables together.

## How to Use It

1. **Create a BOQ**: Add customer, title, and items with quantities/rates
2. **Submit the BOQ**: Change status to submitted  
3. **Make Quotation**: Click the "Create Quotation" button
4. **Convert to Sales Order**: Use standard ERPNext process
5. **Create Project**: Click the "Create Project" button on the BOQ
6. **Check Report**: See everything connected in the BOQ Flow Report

## File Structure (What I Created)

```
apps/boq_manager/
├── boq_manager/
│   ├── doctype/
│   │   ├── bill_of_quantities/
│   │   │   ├── bill_of_quantities.py
│   │   │   └── bill_of_quantities.json
│   │   └── boq_item/
│   │       ├── boq_item.py  
│   │       └── boq_item.json
│   └── hooks.py
```

## Things I Learned

- How to create custom DocTypes in ERPNext
- Using hooks to run code automatically  
- Adding custom fields to existing DocTypes
- Writing Client Scripts for buttons
- Making whitelisted methods for API calls
- Creating Query Reports with SQL
- How parent-child relationships work in Frappe

## Stuff That Could Be Better

- Error handling could be improved (sometimes get confusing error messages)
- Could add more validations  
- UI could look nicer
- Maybe add more fields to track additional info
- Could make the report look better

## Installation

If you want to try this:

1. Create the app: `bench new-app boq_manager`
2. Install it: `bench --site [your-site] install-app boq_manager`  
3. Migrate: `bench --site [your-site] migrate`
4. Restart: `bench restart`

Make sure you have some Items and Customers created first!

## Final Thoughts

This was my first real ERPNext project and I learned a lot! The documentation isn't always clear and I had to ask for help several times, but I'm happy with how it turned out. 

The app actually works and does what it's supposed to do. You can create BOQs, make quotations, and track everything through to projects. Pretty cool for a beginner project!

I know the code isn't perfect but it works and I understand what everything does now. Maybe next time I'll write better code and add more features.

Thanks for checking out my app! 😊
