from django.utils import timezone

def created_at_format(timestamp):
        delta = timezone.now() - timestamp
        if delta.days >= 365:
            years = delta.days // 365
            return f"{years} {'year' if years == 1 else 'years'} ago"
        elif delta.days >= 30:
            months = delta.days // 30
            return f"{months} {'month' if months == 1 else 'months'} ago"
        elif delta.days >= 1:
            return f"{delta.days} {'day' if delta.days == 1 else 'days'} ago"
        elif delta.seconds >= 3600:
            hours = delta.seconds // 3600
            return f"{hours} {'hour' if hours == 1 else 'hours'} ago"
        elif delta.seconds >= 60:
            minutes = delta.seconds // 60
            return f"{minutes} {'minute' if minutes == 1 else 'minutes'} ago"
        else:
            return "just now"