from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Project, ProjectCategory, Favorite, ProjectReview, ProjectRating
from accounts.decorators import role_required


def project_list(request):
    all_projects = Project.objects.all()
    context = {"projects": all_projects}

    if request.user.is_authenticated and hasattr(request.user, "profile"):
        profile = request.user.profile

        created_projects = Project.objects.filter(creator=profile)
        favorited_projects = Project.objects.filter(favorite__profile=profile)
        reviewed_projects = Project.objects.filter(
            projectreview__reviewer=profile
        ).distinct()

        exclude_ids = (
            list(created_projects.values_list("id", flat=True))
            + list(favorited_projects.values_list("id", flat=True))
            + list(reviewed_projects.values_list("id", flat=True))
        )

        context.update({
            "created_projects": created_projects,
            "favorited_projects": favorited_projects,
            "reviewed_projects": reviewed_projects,
            "projects": all_projects.exclude(id__in=exclude_ids),
        })

    return render(request, "diyprojects/project_list.html", context)


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST" and request.user.is_authenticated:
        profile = request.user.profile

        if "favorite_submit" in request.POST:
            favorite = Favorite.objects.filter(
                project=project,
                profile=profile
            ).first()

            if favorite:
                favorite.delete()
            else:
                Favorite.objects.create(
                    project=project,
                    profile=profile,
                    project_status="Backlog"
                )

        elif "rating_submit" in request.POST:
            score = int(request.POST.get("score", 0))

            if 1 <= score <= 10:
                ProjectRating.objects.update_or_create(
                    project=project,
                    profile=profile,
                    defaults={"score": score},
                )

        elif "review_submit" in request.POST:
            ProjectReview.objects.create(
                project=project,
                reviewer=profile,
                comment=request.POST.get("comment"),
                image=request.FILES.get("image")
            )

        return redirect("diyprojects:project_detail", pk=pk)

    average_rating = ProjectRating.objects.filter(project=project).aggregate(
        Avg("score")
    )["score__avg"]

    reviews = ProjectReview.objects.filter(project=project)
    favorites_count = Favorite.objects.filter(project=project).count()

    user_favorited = False
    can_edit = False

    if request.user.is_authenticated:
        profile = request.user.profile
        user_favorited = Favorite.objects.filter(
            project=project,
            profile=profile
        ).exists()

        can_edit = project.creator == profile

    return render(request, "diyprojects/project_detail.html", {
        "project": project,
        "average_rating": average_rating,
        "reviews": reviews,
        "favorites_count": favorites_count,
        "user_favorited": user_favorited,
        "can_edit": can_edit,
    })


@login_required
@role_required("Project Creator")
def project_create(request):
    if request.method == "POST":
        Project.objects.create(
            title=request.POST.get("title"),
            category_id=request.POST.get("category"),
            creator=request.user.profile,
            description=request.POST.get("description"),
            materials=request.POST.get("materials"),
            steps=request.POST.get("steps"),
        )

        return redirect("diyprojects:project_list")

    categories = ProjectCategory.objects.all()

    return render(request, "diyprojects/project_form.html", {
        "categories": categories
    })


@login_required
@role_required("Project Creator")
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if project.creator != request.user.profile:
        return redirect("diyprojects:project_detail", pk=pk)

    if request.method == "POST":
        project.title = request.POST.get("title")
        project.category_id = request.POST.get("category")
        project.description = request.POST.get("description")
        project.materials = request.POST.get("materials")
        project.steps = request.POST.get("steps")
        project.save()

        return redirect("diyprojects:project_detail", pk=project.pk)

    categories = ProjectCategory.objects.all()

    return render(request, "diyprojects/project_form.html", {
        "project": project,
        "categories": categories
    })