from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .models import Images
from .forms import CreateForm
from .forms import ImageForm
from django.contrib.auth.models import User, Group

def home(request):

    return redirect(homepage, pk=1)


def homepage(request, pk):
    items = Item.objects.all()
    images = Images.objects.all()
    pages = 0
    page_list = []
    item = 0
    item_list = [[]]
    for i in items:
        item += 1
        item_list[pages].append(i)
        if item % 36 == 0:
            pages += 1
            page_list.append(pages)
            item_list.append([])
    items = item_list[pk-1]
    page_list.append(pages + 1)
    pages += 1
    if request.POST.get('backpage'):
        return redirect(homepage, pk=int(request.POST.get('backpage'))-1)
    if request.POST.get('nextpage'):
        return redirect(homepage, pk=int(request.POST.get('nextpage'))+1)

    if request.user.groups.filter(name='Модераторы').exists():
        can_create = True
        if request.POST.get('delete'):
            print(request.POST.get('delete'), ' delete')
            Item.objects.filter(id=request.POST.get('delete')).delete()
            list = Images.objects.filter(count=request.POST.get('delete'))
            for i in list:
                i.delete()
    else:
        can_create = False

    return render(request, 'market/homepage.html', {'items': items, 'images': images, 'can_create': can_create, 'page_list': page_list, 'pk': pk, 'pages': pages})


def item_page(request, pk):
    item = get_object_or_404(Item, pk=pk)
    images = Images.objects.filter(count=pk)
    if request.user.groups.filter(name='Модераторы').exists():
        can_create = True
        if request.POST.get('delete'):
            print(request.POST.get('delete'), ' delete')
            Item.objects.filter(id=request.POST.get('delete')).delete()
            list = Images.objects.filter(count=request.POST.get('delete'))
            for i in list:
                i.delete()
        if request.POST.get('red'):
            return redirect(edit, pk=pk)
    else:
        can_create = False

    return render(request, 'market/item_page.html', {'item': item, 'images': images, 'can_create': can_create})


def edit(request, pk):
    item = get_object_or_404(Item, id=pk)
    images = Images.objects.filter(count=pk)
    if request.user.groups.filter(name='Модераторы').exists():
        can_create = True
        if request.POST.get('save'):
            form = CreateForm(request.POST)
            imgform = ImageForm(request.POST)
            imglist = []
            if form.is_valid():
                try:
                    price = int(form.cleaned_data.get('price'))
                except:
                    return render(request, "market/edit.html", {'images': images, 'item': item, 'form': form, 'imgform': imgform, 'can_create': can_create})
                images = 0  #request.FILES.getlist('image')
                if request.FILES.getlist('image') != []:
                    images = request.FILES.getlist('image')
                    imgnorm = ['.jpg', '.png', 'jpeg']
                    imglist = []
                    for i in images:
                        if str(i)[-4:] in imgnorm:
                            imglist.append(i)
                        else:
                            error = 'Только типы: jpeg, jpg, png'
                            return render(request, "market/edit.html", {'images': images, 'item': item, 'form': form, 'imgform': imgform, 'error': error, 'can_create': can_create})
                if can_create:
                    new = Item.objects.get(id=pk)
                    new.brand = form.cleaned_data.get('brand')
                    new.name = form.cleaned_data.get('name')
                    new.color = form.cleaned_data.get('color')
                    new.category = form.cleaned_data.get('category')
                    new.sec_category = form.cleaned_data.get('sec_category')
                    new.price = form.cleaned_data.get('price')
                    new.info = form.cleaned_data.get('info')
                    new.save()

                    if imglist != []:
                        Images.objects.filter(count=new.id).delete()
                        Images.objects.create(count=new.id, is_active=1,image=imglist[0])
                        imglist.remove(imglist[0])
                        for i in imglist:
                            Images.objects.create(count=new.id, is_active=0, image=i)

                return redirect(item_page, pk=new.id)
            else:
                return render(request, "market/edit.html", {'images': images, 'item': item, 'form': form, 'imgform': imgform, 'can_create': can_create})
        if request.POST.get('img_add'):
            print('True')
            form = CreateForm(request.POST)
            imgform = ImageForm(request.POST)
            img_add = True

            return render(request, "market/edit.html",
                          {'images': images, 'item': item, 'form': form, 'imgform': imgform, 'can_create': can_create,
                           'img_add': img_add})

        else:
            form = CreateForm(request.POST)
            imgform = ImageForm(request.POST)
            img_add = False

            return render(request, "market/edit.html", {'images': images, 'item': item, 'form': form, 'imgform': imgform, 'can_create': can_create, 'img_add': img_add})
    else:
        can_create = False
    return render(request, 'market/edit.html', {'images': images, 'item': item, 'can_create': can_create})


def create(request):
    if request.user.groups.filter(name='Модераторы').exists():
        can_create = True
        if request.method == "POST":
            form = CreateForm(request.POST)
            imgform = ImageForm(request.POST)
            if form.is_valid():
                try:
                    price = int(form.cleaned_data.get('price'))
                except:
                    return render(request, "market/create.html", {'form': form, 'imgform': imgform, 'can_create': can_create})
                images = request.FILES.getlist('image')
                print(images)
                imgnorm = ['.jpg', '.png', 'jpeg']
                imglist = []
                for i in images:
                    if str(i)[-4:] in imgnorm:
                        imglist.append(i)
                    else:
                        error = 'Только типы: jpeg, jpg, png'
                        return render(request, "market/create.html", {'form': form, 'imgform': imgform, 'error': error, 'can_create': can_create})
                if can_create:
                    new = Item.objects.create(
                        brand=form.cleaned_data.get('brand'),
                        name=form.cleaned_data.get('name'),
                        color=form.cleaned_data.get('color'),
                        category=form.cleaned_data.get('category'),
                        sec_category=form.cleaned_data.get('sec_category'),
                        price=form.cleaned_data.get('price'),
                        info=form.cleaned_data.get('info'),
                        img_count=0
                    )
                    Images.objects.create(count=new.id, is_active=1,image=imglist[0])
                    imglist.remove(imglist[0])
                    for i in imglist:
                        Images.objects.create(count=new.id, is_active=0, image=i)

                return redirect(item_page, pk=new.id)
            else:
                return render(request, "market/create.html", {'form': form, 'imgform': imgform, 'can_create': can_create})
        else:
            form = CreateForm(request.POST)
            imgform = ImageForm(request.POST)

            return render(request, "market/create.html", {'form': form, 'imgform': imgform, 'can_create': can_create})
    else:
        can_create = False

    return render(request, "market/create.html", {'can_create': can_create})