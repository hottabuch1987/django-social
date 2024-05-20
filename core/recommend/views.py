from django.shortcuts import redirect, render
from .models import Review


def delete_review(request, review_id):
    review = Review.objects.get(id=review_id)
    
    if request.user == review.created_by:
        review.delete()
        return redirect('account:dashboard')
        # Можно добавить дополнительную логику или сообщение об успешном удалении
    return redirect('account:dashboard')  

