import phonenumbers
from phonenumbers import timezone, geocoder, carrier

# Taking user input for the phone number with country code
number = input("Enter phone number with country code (e.g., +919876543210): ")

try:
    # Parsing the input string into a phone number object
    phoneNumber = phonenumbers.parse(number)

    # Validating if the number is possible
    if not phonenumbers.is_valid_number(phoneNumber):
        print("Invalid phone number! Please enter a valid number.")
    else:
        # Fetching timezone
        timeZone = timezone.time_zones_for_number(phoneNumber)
        print("Timezone:", timeZone)

        # Fetching geographical location
        geolocation = geocoder.description_for_number(phoneNumber, "en")
        print("Location:", geolocation)

        # Fetching service provider
        service = carrier.name_for_number(phoneNumber, "en")
        print("Service provider:", service)

except phonenumbers.phonenumberutil.NumberParseException:
    print("Invalid input! Please enter the number in correct format (e.g., +919876543210).")
