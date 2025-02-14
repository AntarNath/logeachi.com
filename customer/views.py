from django.shortcuts import render, redirect, get_object_or_404
from customer.models import Address
from accounts.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from utils.image_resizer import resize_image
from django.core.paginator import Paginator

# Create your views here.
@login_required
def user_dashboard(request):
    orders = orders = request.user.get_order()[:5]
    context = {
        'orders': orders,
    }
    return render(request, 'customer/dashboard.html', context)


@login_required
def address_book(request):
    addresses = Address.objects.all()
    return render(request, 'customer/address_book.html', {'addresses': addresses})


@login_required
def add_address(request):
    
    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_number = request.POST.get('phone_number')
            details_address = request.POST.get('details_address')
            zila = request.POST.get('zila')
            thana = request.POST.get('thana')
            postal_code = request.POST.get('postal_code')
            shipping_address = request.POST.get('shipping_address')
            billing_address = request.POST.get('billing_address')
            both_address = request.POST.get('both_address')
            user = request.user 
               
            if billing_address:
                
                 # finding addresses to set false in the billing addresses
                already_addresses = Address.objects.filter(user=user)
                
                if already_addresses:
                    for already_address in already_addresses:
                        already_address.is_default_billing=False
                        already_address.save()
                
                billing_address = True
                
            else:
                billing_address = False
                    
            if shipping_address:
                # finding addresses to set false in the shipping addresses
                already_addresses = Address.objects.filter(user=user)
                
                if already_addresses:
                    for already_address in already_addresses:
                        already_address.is_default_shipping=False
                        already_address.save()

                shipping_address = True
            
            else:
                shipping_address=False
               
            Address.objects.create(user=user, first_name=first_name, last_name=last_name, 
                phone_number=phone_number, details_address=details_address, 
                zila=zila, thana=thana, postal_code=postal_code, is_default_billing=billing_address,
                is_default_shipping=shipping_address
            )
            
            messages.success(request, 'Address created successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        
        except Exception as e:
            messages.error(request, f'{e}')
            return redirect(request.META.get('HTTP_REFERER'))

    return render(request, 'customer/add_address.html')


@login_required
def edit_address(request):
    if request.method == 'POST':
        try:
            address_id = request.POST.get('address_id')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_number = request.POST.get('phone_number')
            details_address = request.POST.get('details_address')
            zila = request.POST.get('zila')
            thana = request.POST.get('thana')
            postal_code = request.POST.get('postal_code')
            shipping_address = request.POST.get('shipping_address')
            billing_address = request.POST.get('billing_address')
            user = request.user
            
            # get the address by id
            address = Address.objects.get(id=address_id)
            
            if address:
   
                if billing_address:
                    
                    # finding addresses to set false in the billing addresses
                    already_addresses = Address.objects.filter(user=user)
                    if already_addresses:
                        for already_address in already_addresses:
                            already_address.is_default_billing=False
                            already_address.save()
                    
                    billing_address = True
                    
                else:
                    billing_address = False


                if shipping_address:
                    
                    # finding addresses to set false in the shipping addresses
                    already_addresses = Address.objects.filter(user=user)
                    if already_addresses:
                        for already_address in already_addresses:
                            already_address.is_default_shipping=False
                            already_address.save()
                    
                    shipping_address = True
                    
                else:
                    shipping_address = False

                address.first_name=first_name
                address.last_name=last_name
                address.phone_number=phone_number
                address.details_address=details_address
                address.zila=zila
                address.thana=thana
                address.postal_code=postal_code
                address.is_default_billing=billing_address
                address.is_default_shipping=shipping_address
                address.save()

                messages.success(request, 'Address Edited successfully')
                return redirect('address_book')
            
            else:
                messages.error(request, 'Address not found')
                return redirect(request.META.get('HTTP_REFERER'))

        except Exception as e:
            messages.error(request, f'{e}')
            return redirect(request.META.get('HTTP_REFERER'))
 
    else:   
        address_id = request.GET.get('address_id')
        address = Address.objects.get(id=address_id)
        return render(request, 'customer/edit_address.html', {'address': address})


@login_required
def delete_address(request):
    
    if request.method == 'GET':
        try:
            address_id = request.GET.get('address_id')
            address = get_object_or_404(Address, id=address_id)
            address.delete()
            
            messages.success(request, 'Address Deleted successfully')
            return redirect(request.META.get('HTTP_REFERER'))

        except Exception as e:
            messages.error(request, f'{e}')
            return redirect(request.META.get('HTTP_REFERER'))
        
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def default_shipping(request):
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        user = request.user
        try:
            # Update the default shipping address for the user
            Address.objects.filter(user=user, is_default_shipping=True).update(is_default_shipping=False)
            address = Address.objects.get(id=address_id, user=user)
            address.is_default_shipping = True
            address.save()
            
            messages.success(request, 'Default Billing Address Changed successfully')
        except Exception as e:
            messages.error(request, f'{e}')
        
        return redirect(request.META.get('HTTP_REFERER'))
    
    addresses = Address.objects.all()
    return render(request, 'customer/make_default_shipping_address.html', {'addresses': addresses})


@login_required
def deafult_billing(request):
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        user = request.user
        try:
            # Update the default billing address for the user
            Address.objects.filter(user=user, is_default_billing=True).update(is_default_billing=False)
            address = Address.objects.get(id=address_id, user=user)
            address.is_default_billing = True
            address.save()
            
            messages.success(request, 'Default Billing Address Changed successfully')
        except Exception as e:
            messages.error(request, f'{e}')
        
        return redirect(request.META.get('HTTP_REFERER'))
    
    addresses = Address.objects.all()
    return render(request, 'customer/make_default_billing_address.html', {'addresses': addresses})


@login_required
def profileView(request):
    return render(request, 'customer/profile.html')


@login_required
def edit_profile(request):
    
    if request.method =='POST':
        try:
            # get profile edit data
            email = request.user.email
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            gender = request.POST.get('gender')
            birthdate = request.POST.get('birthdate')
            phone_number = request.POST.get('phone_number')
            user_image =  request.FILES.get('user_image')
            
            # get user by email address
            user = User.objects.get(email=email)
            
            # Updateing the user object
            user.first_name = first_name
            user.last_name = last_name
            user.gender = gender
            if birthdate:
                user.birthdate = birthdate
            if phone_number:
                user.phone_number = phone_number
            if user_image:
                # print('===============================================================', user_image)
                resized_user_image = resize_image(user_image, 165, 165)
                user.user_image = resized_user_image
            user.save()
            
            messages.success(request, 'Profile Updated Successfully')
        
        except Exception as e:
            messages.error(request, f'{e}')
            
        return redirect('profile')

    return render(request, 'customer/edit_profile.html')


@login_required
def order(request):
    orders = request.user.get_order()
    paginator = Paginator(orders, 5)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    context = {
        'orders': orders
    }
    return render(request, 'customer/my_order.html', context) 