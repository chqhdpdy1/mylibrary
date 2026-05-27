"""
=================================================================
[과제 3] books/models.py
클래스메서드와 함수 리턴타입을 이용한 간단한 책 대여 서비스
=================================================================
"""

from django.db import models
from django.db.models import QuerySet


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} by {self.author}"

    # ──────────────────────────────────────────────────────────────
    # [1-1] 전체 책 목록 반환
    # ──────────────────────────────────────────────────────────────
    @classmethod
    def get_all_books(cls) -> QuerySet['Book']:
        """
        전체 책 목록 반환
        """
        return cls.objects.all()

    # ──────────────────────────────────────────────────────────────
    # [1-2] 특정 저자의 책만 반환 (대소문자 구분 없는 정확 일치)
    # ──────────────────────────────────────────────────────────────
    @classmethod
    def get_books_by_author(cls, author_name) -> QuerySet['Book']:
        """
        특정 저자의 책만 반환 (대소문자 구분 없이 정확 일치)
        """
        return cls.objects.filter(author__iexact=author_name)

    # ──────────────────────────────────────────────────────────────
    # [1-3] 제목에 키워드가 포함된 책 반환 (대소문자 구분 없는 부분 일치)
    # ──────────────────────────────────────────────────────────────
    @classmethod
    def get_books_by_title_keyword(cls, keyword) -> QuerySet['Book']:
        """
        제목에 키워드가 포함된 책 반환 (대소문자 구분 없이)
        """
        return cls.objects.filter(title__icontains=keyword)

    # ──────────────────────────────────────────────────────────────
    # [1-4] 제목 순으로 정렬된 책 목록 반환
    # ──────────────────────────────────────────────────────────────
    @classmethod
    def get_books_ordered_by_title(cls) -> QuerySet['Book']:
        """
        제목 순으로 정렬된 책 목록 반환
        """
        return cls.objects.all().order_by('title')
