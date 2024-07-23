import logging

logger = logging.getLogger(__name__)

def handle_error(error, ctx):
    """
    Handles errors and displays informative messages to users.

    Args:
        error (Exception): The exception that occurred.
        ctx (commands.Context): The Discord context object.
    """
    logger.error(f"An error occurred: {error}")
    try:
        await ctx.send(f"An error occurred: {error}")
    except discord.HTTPException:
        logger.error("Failed to send error message to Discord.")