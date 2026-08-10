const BUTTONDOWN_SUBSCRIBERS_URL = "https://api.buttondown.com/v1/subscribers";

export default {
  async formSubmitted(event) {
    const formName = event.data["form-name"] ?? event.data.form_name;

    if (formName !== "bulletin-subscribe") {
      return;
    }

    const emailAddress = event.data.email?.trim().toLowerCase();
    const apiKey = process.env.BUTTONDOWN_API_KEY;

    if (!emailAddress) {
      throw new Error("The bulletin subscription did not include an email address.");
    }

    if (!apiKey) {
      throw new Error(
        "BUTTONDOWN_API_KEY is not configured. The submission remains available in Netlify for retry."
      );
    }

    const response = await fetch(BUTTONDOWN_SUBSCRIBERS_URL, {
      method: "POST",
      headers: {
        Authorization: `Token ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email_address: emailAddress }),
    });

    if (!response.ok) {
      const responseBody = await response.text();
      throw new Error(
        `Buttondown rejected the subscription (${response.status}): ${responseBody}`
      );
    }
  },
};
