import discord
import requests


class Channel(discord.TextChannel):

    @property
    def send_webhook(self, url, content=None, embed=None):
        """
        Send a response to a webhook.

        Args:
            url (str): The webhook URL to send the message to.
            content (str, optional): The content of the message.
            embed (discord.Embed, optional): The embed to include with the message.

        Returns:
            Response: The response from the webhook request.
        """
        # Initialize response variable

        response = None

        if embed and content:
            response = requests.post(url, content=content, json={"embeds": [embed.to_dict()]})
        elif embed:
            response = requests.post(url, json={"embeds": [embed.to_dict()]})
        elif content:
            response = requests.post(url, content=content)

        if response and response.status_code == 204:
            return response
        else:

            if response is not None:
                print(f"Error sending webhook: {response.status_code} - {response.text}")
            else:
                print("No response received.")
            return None

