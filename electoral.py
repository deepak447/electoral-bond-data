import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("/mnt/d/work/projects/electoral_bond/final_data.csv")

# App title
st.markdown(
    """
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <h1 class="display-3 text-center text-primary" style="font-family: 'Arial', sans-serif; font-weight: bold; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);">Electoral Bond Data Visualization</h1>
    """,
    unsafe_allow_html=True,
)
st.markdown("<br>",unsafe_allow_html=True)
st.markdown("<br>",unsafe_allow_html=True)
# ---------------------------------------Select Parties--------------------------------------------------------------
party_name = df["Name of the Political Party"].unique()
st.subheader("Company Bond Purchases")
name = st.selectbox("Enter the party name", party_name, index=None)
party_data = df[df["Name of the Political Party"] == name]

submit = st.button("click button",key="party_data")
if submit:
    if name is None:
        st.markdown("Please Select Party")
    else:
        company_bonds = party_data.groupby("Name of the Purchaser")["Denominations_x"].sum()
        total_bonds = party_data["Denominations_x"].sum()
         # Format amounts for display (in crores)
        #company_bonds_cr = company_bonds / 100000
        amount_cr = total_bonds / 10000000
        table = pd.DataFrame( company_bonds )
        st.write(table)
        st.markdown(f"Total amount : {amount_cr} cr")
st.markdown("<br>",unsafe_allow_html=True)
st.markdown("<br>",unsafe_allow_html=True)

# ------------------------------------------Select company-------------------------------------------------------

st.subheader("Parties Donation Received ")
company_name = df["Name of the Purchaser"].unique()
selected_company = st.selectbox("Select Company", company_name,index=None)

# Filter data by selected company
company_data = df[df["Name of the Purchaser"] == selected_company]  # Use df here, not party_data

# Get all parties that received donations from this company
parties_with_donations = company_data["Name of the Political Party"].unique()

submit2 = st.button("Click",key="submit2")

if submit2:
    if selected_company is None:
        st.write("Please select Company")
        # Display table
    else:

        st.subheader("Bond Purchases by Company")
        table = pd.DataFrame(company_data[["Name of the Political Party","Bond\nNumber", "Denominations_x"]])
        table.columns = ["Name of the Political Party","Bond Number", "Total Bond Amount"]
        st.dataframe(table)

        # Display total bonds for the party
        total_bonds = company_data["Denominations_x"].sum()
        amount_cr = total_bonds / 10000000
        st.markdown(f"**Total Bonds Purchased by {selected_company}:** {amount_cr} cr")
st.markdown("<br>",unsafe_allow_html=True)
st.markdown("<br>",unsafe_allow_html=True)


#------------------------------------------- Parties and company-------------------------------------------------
st.subheader("Party and Company Specific Bond Purchases")
col1, col2 = st.columns(2)

# Party selection in column 1
with col1:
    party_name = df["Name of the Political Party"].unique()
    selected_party = st.selectbox("Select Party", party_name, key="input1", index=None)

# Company selection in column 2
with col2:
    company_name = df["Name of the Purchaser"].unique()
    selected_company = st.selectbox("Select Company", company_name, key="input2", index=None)

# Display results
if selected_party and selected_company:
    # Filter data based on selected party and company
    filtered_data = df[
        (df["Name of the Political Party"] == selected_party)
        & (df["Name of the Purchaser"] == selected_company)
    ]

    # Calculate total amount received
    total_amount = filtered_data["Denominations_x"].sum()
    _amount_cr = total_amount / 10000000
    if total_amount == 0:
        st.write("Bond Not Purchase ")
    else:


        # Display total amount
        st.markdown(
            f"Total amount received by {selected_party} from {selected_company}   :  **{_amount_cr} cr**"
        )
st.markdown("<br>",unsafe_allow_html=True)
st.markdown("<br>",unsafe_allow_html=True)

# --- Comparison b/w Parties --------------------------------------------------------------------------------
st.subheader("Comparison of Donations Received to Parties (Bar Chart)")
# Create columns
col1, col2 = st.columns(2)

# Party selection in column 1
with col1:
    party_name = df["Name of the Political Party"].unique()
    selected_party1 = st.selectbox("Select Party 1", party_name, key="input4", index=None)

# Company selection in column 2
with col2:
    party_name = df["Name of the Political Party"].unique()
    selected_party2 = st.selectbox("Select Party 2", party_name, key="input5", index=None)


# -------------------------- Bar Chart (for selected party) ----------------------------------------------
input = st.button("click..",key="input")
if input:
    if selected_party1 and selected_party2:
        # Filter data based on selected parties
        party1_data = df[df["Name of the Political Party"] == selected_party1]
        party2_data = df[df["Name of the Political Party"] == selected_party2]

        # Calculate total amount received by each party (across all companies)
        total_party1_amount = party1_data["Denominations_x"].sum()
        total_party2_amount = party2_data["Denominations_x"].sum()

        # Format amounts for display (in crores)
        total_party1_amount_cr = total_party1_amount / 10000000  # Divide by 1 crore
        total_party2_amount_cr = total_party2_amount / 10000000

        # Create a dataframe for plotting
        plot_data = pd.DataFrame({
            "Party": [selected_party1, selected_party2],
            "Total Amount Received (Cr)": [total_party1_amount_cr, total_party2_amount_cr]
        })

        # Create bar chart
        fig, ax = plt.subplots()
        ax.bar(plot_data["Party"], plot_data["Total Amount Received (Cr)"], width=0.3)  

        # Chart customizations
        ax.set_xlabel("Political Party")
        ax.set_ylabel("Total Amount Received (Cr)")
        ax.set_title(f"Comparison of Donations Received by {selected_party1} and {selected_party2}")
        st.pyplot(fig)

        # Display amounts in crores for clarity
        st.write(f"{selected_party1}: {total_party1_amount_cr:.2f} Cr")
        st.write(f"{selected_party2}: {total_party2_amount_cr:.2f} Cr")

    else:
        st.markdown(f"Please Select Party First")


st.subheader("Pie Chart: Party Donations by Company")

company_name = df["Name of the Purchaser"].unique()
selected_company = st.selectbox("Select Company", company_name,key="data", index=None)

submit_pie = st.button("Generate Pie Chart", key="submit_pie")

if submit_pie:
    if selected_company is None:
        st.write("Please select a Company")
    else:
        company_data = df[df["Name of the Purchaser"] == selected_company]
        party_donations = company_data.groupby("Name of the Political Party")["Denominations_x"].sum()

        # Filter parties with donations above 1 crore
        party_donations = party_donations[party_donations > 10000000]

        # Convert values to crores
        party_donations_cr = party_donations / 10000000  

        df_donation = pd.DataFrame(party_donations_cr)

        # Create the pie chart
        fig, ax = plt.subplots(figsize=(8, 8))  # Adjust figure size as needed
        ax.pie(df_donation["Denominations_x"], labels=df_donation.index, autopct='%1.1f%%', startangle=32)
        ax.axis('equal')  # Equal aspect ratio ensures a circular pie chart

        # Customize labels to prevent overlapping
        plt.tight_layout()  # Adjust layout to avoid label clipping
        plt.subplots_adjust(left=0.1, bottom=0.2, right=0.8, top=0.9, wspace=0.5, hspace=0.5)

        # Display the chart
        st.pyplot(fig)