from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count, Avg
from django.urls import path
import json


from .models import Application, SponsoredChild, AcademicReport
GRADE_MAP = {
    "A": 12, "A-": 11, "B+": 10, "B": 9, "B-": 8,
    "C+": 7, "C": 6, "C-": 5, "D+": 4, "D": 3, "D-": 2, "E": 1
}

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'county', 'status', 'created_at')
    list_filter = ('status', 'county')
    search_fields = ('full_name', 'email', 'phone_number')


@admin.register(SponsoredChild)
class SponsoredChildAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'guardian_name', 'current_school', 'active')
    search_fields = ('full_name', 'guardian_name', 'current_school')
    list_filter = ('active', 'current_school')


@admin.register(AcademicReport)
class AcademicReportAdmin(admin.ModelAdmin):
    list_display = ('child', 'term', 'year', 'average_grade', 'uploaded_at')
    list_filter = ('term', 'year', 'child__current_school')
    search_fields = ('child__full_name',)


# ---- Custom Dashboard View ----
@staff_member_required
def foundation_dashboard(request):
    # Chart 1: Children per County
    county_data = SponsoredChild.objects.values('county').annotate(total=Count('id')).order_by('county')
    counties = [c['county'] for c in county_data]
    child_counts = [c['total'] for c in county_data]

    # Chart 2: Average grade per term (manual mapping)
    term_reports = AcademicReport.objects.values('term', 'average_grade')
    term_scores = {}
    for r in term_reports:
        grade = GRADE_MAP.get(r['average_grade'], 0)
        term_scores.setdefault(r['term'], []).append(grade)
    terms = list(term_scores.keys())
    avg_grades = [round(sum(scores)/len(scores), 2) for scores in term_scores.values()]

    # Chart 3: Top Performing Schools (manual mapping)
    school_reports = AcademicReport.objects.select_related('child')
    school_scores = {}
    for r in school_reports:
        if r.child and r.child.current_school:
            grade = GRADE_MAP.get(r.average_grade, 0)
            school_scores.setdefault(r.child.current_school, []).append(grade)
    school_avg = {school: round(sum(scores)/len(scores), 2) for school, scores in school_scores.items()}
    sorted_schools = sorted(school_avg.items(), key=lambda x: x[1], reverse=True)[:5]
    schools = [s[0] for s in sorted_schools]
    school_performance = [s[1] for s in sorted_schools]

    return render(request, 'admin/foundation_dashboard.html', {
    'counties': json.dumps(counties),
    'child_counts': json.dumps(child_counts),
    'terms': json.dumps(terms),
    'avg_grades': json.dumps(avg_grades),
    'schools': json.dumps(schools),
    'school_performance': json.dumps(school_performance),
})
