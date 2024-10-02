from setuptools import setup, find_packages

setup(
    name='spider-ai',                     # اسم المكتبة
    version='0.4',                      # الإصدار الأول
    packages=find_packages(),             # البحث عن الحزم
    install_requires=[],                  # المتطلبات (إن وجدت)
    description='Lib python for powerful AI',  # وصف المكتبة
    long_description=open('README.md').read(),  # شرح مفصل من ملف README.md
    long_description_content_type='text/markdown',  # نوع المحتوى للشرح
    author='spiderXR',                   # اسمك
    author_email='mostshariblis@gmail.com', # بريدك الإلكتروني
    url='https://github.com/loverelyas/spider-ai', # رابط GitHub الخاص بالمشروع
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # دعم بايثون من إصدار 3.6 فما فوق
)
