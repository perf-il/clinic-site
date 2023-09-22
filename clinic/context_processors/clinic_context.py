from clinic.models import Direction


def directions_for_top(request):
    directions = Direction.objects.order_by('title')
    return {
        'list_directions': directions
    }