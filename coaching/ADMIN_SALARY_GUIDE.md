# How to Add/Edit Salary in Django Admin

## Steps

1. **Go to Django Admin**
   - Open your browser to `/admin/`

2. **Navigate to Users**
   - Click on “Users” under the “Authentication and Authorization” section

3. **Select a User**
   - Click on any user (teacher or other role) you want to edit

4. **Edit Salary Fields**
   - In the edit form, scroll down to the **Salary** section
   - You will see two fields:
     - **Salary pending**: checkbox (True = Pending, False = Paid)
     - **Salary till date**: date picker (sets the till date)

5. **Save Changes**
   - Scroll to the bottom and click “Save”
   - The user’s salary status and till date will be updated

## What the Fields Mean

- **Salary pending**:
  - Checked = Salary is **Pending**
  - Unchecked = Salary is **Paid**

- **Salary till date**:
  - Leave blank for no till date
  - Pick a date to set the salary till date

## Tips

- You can also edit directly from the Users list:
  - Go to `/admin/`
  - In the Users list, hover over a row → click “Edit”
  - Change “Salary pending” and/or “Salary till date”
  - Click “Save”

## Result

- The Salary page (`/salary/`) will reflect your changes immediately
- Admin dashboard Salary link shows updated status and till date

---

*If you don’t see the “Salary” section in the edit form, restart the Django development server.*
