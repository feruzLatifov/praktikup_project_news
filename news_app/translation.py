from modeltranslation.translator import register, TranslationOptions, translator
from .models import News, Category

@register(News) #1-usul
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'body')

# #2-usul
# translator.register(News, NewsTranslationOptions)

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)