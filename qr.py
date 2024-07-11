import qrcode

# URL of the PDF file on your custom domain
pdf_url = "https://lednits.com/LedNits%20Led%20Screen%20Manufacturers.pdf"

# Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(pdf_url)
qr.make(fit=True)

# Create an image from the QR code
qr_img = qr.make_image(fill_color="black", back_color="white")

# Save or display the QR code image
qr_img.save("menu_qr_code.png")
