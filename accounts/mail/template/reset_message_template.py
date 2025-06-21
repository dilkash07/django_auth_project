def reset_emai_message_template(user, reset_url):
    return f"""
    <!DOCTYPE html>
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi {user.first_name},</p>

        <p>We know it can be frustrating to lose access to your account. Don't worry, we're here to help!</p>

        <p>Here's how to reset your password:</p>
        <ul>
          <li>Click this link: <a href="{reset_url}" style="color: #1a73e8;">Reset Password</a></li>
          <li>Follow the on-screen instructions.</li>
        </ul>

        <p>If you encounter any issues or have questions, please reach out to our support team at 
          <a href="mailto:caremansurimart@gmail.com" style="color: #1a73e8;">caremansurimart@gmail.com</a>.
        </p>

        <p>We'll do our best to get you back into your account quickly.</p>

        <p>Best regards,<br>
        The MansuriMart Team</p>
      </body>
    </html>
    """
