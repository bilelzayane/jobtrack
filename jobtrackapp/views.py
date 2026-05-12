from django.core.paginator import Paginator
from django.db.models import Q
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import ApplicationForm, AdminApplicationForm, CompanyForm, OfferForm
from .models import Application, Company, Offer


def index(request):
    offers_count = (
        Offer.objects.count()
        if request.user.is_authenticated
        else Offer.objects.filter(status="Open").count()
    )
    return render(
        request,
        "jobtrack/index.html",
        {
            "companies_count": Company.objects.count(),
            "offers_count": offers_count,
            "applications_count": Application.objects.count(),
        },
    )


def offer_list(request):
    qs = Offer.objects.select_related("company").all().order_by("-posted_at")
    if not request.user.is_authenticated:
        qs = qs.filter(status="Open")
    q = request.GET.get("q", "")
    status = request.GET.get("status", "")
    otype = request.GET.get("type", "")
    if q:
        qs = qs.filter(
            Q(title__icontains=q)
            | Q(company__name__icontains=q)
            | Q(location__icontains=q)
        )
    if status and status != "All statuses":
        qs = qs.filter(status=status)
    if otype and otype != "All types":
        qs = qs.filter(type=otype)
    total_offers = qs.count()
    paginator = Paginator(qs, 8)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "jobtrack/offers/list.html",
        {
            "offers": page_obj,
            "page_obj": page_obj,
            "total_offers": total_offers,
            "query": q,
        },
    )


def offer_detail(request, pk):
    if request.user.is_authenticated:
        offer = get_object_or_404(Offer, pk=pk)
    else:
        offer = get_object_or_404(Offer, pk=pk, status="Open")
    applications = offer.applications.all()
    return render(
        request,
        "jobtrack/offers/detail.html",
        {"offer": offer, "applications": applications},
    )


@login_required
def offer_new(request):
    form = OfferForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        offer = form.save(commit=False)
        offer.author = request.user
        offer.save()
        return redirect("jobtrack:offers")
    return render(
        request, "jobtrack/offers/form.html", {"form": form, "action": "Create"}
    )


@login_required
def offer_edit(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    form = OfferForm(request.POST or None, instance=offer)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("jobtrack:offer_detail", pk=offer.pk)
    return render(
        request,
        "jobtrack/offers/form.html",
        {"form": form, "offer": offer, "action": "Save"},
    )


@login_required
def offer_delete(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if request.method == "POST":
        offer.delete()
        return redirect("jobtrack:offers")
    return render(request, "jobtrack/offers/confirm_delete.html", {"offer": offer})


def company_list(request):
    q = request.GET.get("q", "")
    companies = Company.objects.all().order_by("name")
    if q:
        companies = companies.filter(
            Q(name__icontains=q) | Q(industry__icontains=q) | Q(location__icontains=q)
        )
    paginator = Paginator(companies, 6)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "jobtrack/companies/list.html",
        {"companies": page_obj, "page_obj": page_obj, "query": q},
    )


def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.user.is_authenticated:
        offers = company.offers.all()
    else:
        offers = company.offers.filter(status="Open")
    return render(
        request,
        "jobtrack/companies/detail.html",
        {"company": company, "offers": offers},
    )


@login_required
def company_new(request):
    form = CompanyForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        company = form.save(commit=False)
        company.author = request.user
        company.save()
        return redirect("jobtrack:companies")
    return render(
        request, "jobtrack/companies/form.html", {"form": form, "action": "Create"}
    )


@login_required
def company_edit(request, pk):
    company = get_object_or_404(Company, pk=pk)
    form = CompanyForm(request.POST or None, request.FILES or None, instance=company)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("jobtrack:company_detail", pk=company.pk)
    return render(
        request,
        "jobtrack/companies/form.html",
        {"form": form, "company": company, "action": "Save"},
    )


@login_required
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == "POST":
        company.delete()
        return redirect("jobtrack:companies")
    return render(
        request, "jobtrack/companies/confirm_delete.html", {"company": company}
    )


@login_required
def application_list(request):
    applications = (
        Application.objects.select_related("offer", "offer__company")
        .all()
        .order_by("-id")
    )
    paginator = Paginator(applications, 8)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "jobtrack/applications/list.html",
        {"applications": page_obj, "page_obj": page_obj},
    )


@login_required
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)
    return render(
        request, "jobtrack/applications/detail.html", {"application": application}
    )


def application_new(request):
    if request.user.is_authenticated:
        form = AdminApplicationForm(request.POST or None, request.FILES or None)
    else:
        form = ApplicationForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        if request.user.is_authenticated:
            return redirect("jobtrack:applications")
        return redirect("jobtrack:offers")
    return render(
        request, "jobtrack/applications/form.html", {"form": form, "action": "Submit"}
    )


@login_required
def application_edit(request, pk):
    application = get_object_or_404(Application, pk=pk)
    form = AdminApplicationForm(
        request.POST or None, request.FILES or None, instance=application
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("jobtrack:application_detail", pk=application.pk)
    return render(
        request,
        "jobtrack/applications/form.html",
        {"form": form, "application": application, "action": "Save"},
    )


@login_required
def download_cv(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if not application.cv_file:
        raise Http404
    return FileResponse(
        application.cv_file.open("rb"),
        as_attachment=True,
        filename=application.cv_file.name.split("/")[-1],
    )


@login_required
def application_delete(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if request.method == "POST":
        application.delete()
        return redirect("jobtrack:applications")
    return render(
        request,
        "jobtrack/applications/confirm_delete.html",
        {"application": application},
    )
