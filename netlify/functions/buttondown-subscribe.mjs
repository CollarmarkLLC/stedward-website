const BUTTONDOWN_SUBSCRIBERS_URL = "https://api.buttondown.com/v1/subscribers";

export default {
  async formSubmitted(event) {
    console.info("Buttondown relay received a verified form submission.");

    const submissionKind = event.data["submission-kind"];

    if (submissionKind !== "bulletin-subscribe") {
      console.info("Buttondown relay ignored a non-bulletin submission.");
      return;
    }

    const emailAddress = event.data.email?.trim().toLowerCase();
    const apiKey = process.env.BUTTONDOWN_API_KEY;

    if (!emailAddress) {
      console.error("Buttondown relay rejected a bulletin submission without an email address.");
      throw new Error("The bulletin subscription did not include an email address.");
    }

    if (!apiKey) {
      console.error("Buttondown relay cannot run because its API credential is unavailable.");
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
      console.error(`Buttondown rejected the subscription with HTTP ${response.status}.`);
      throw new Error(
        `Buttondown rejected the subscription with HTTP ${response.status}.`
      );
    }

    console.info("Buttondown accepted the bulletin subscription.");
  },
};
