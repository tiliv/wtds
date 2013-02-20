import logging

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.contenttypes.models import ContentType

from wtds.core.views import AuthenticationMixin
from .models import Report
from .forms import ReportForm

logger = logging.getLogger(__name__)

class ReportMixin(AuthenticationMixin):
    model = Report

    target_content_type = None
    target_model_class = None
    target_model_field_name = None
    target_model_instance_pk = None
    target_model_instance = None

    def dispatch(self, request, *args, **kwargs):
        self._resolve_target(request, kwargs)
        return super(ReportMixin, self).dispatch(request, *args, **kwargs)

    def _resolve_target(self, request, kwargs):
        """
        Sets the view's attributes if the corresponding url keyword arguments are available:

        * content type (and model class, by association)
        * field name
        * instance

        """

        instance_name = request.resolver_match.app_name # dispatch from embedded app urls
        if instance_name or 'contenttype' in kwargs:
            if instance_name:
                model = instance_name
            elif 'contenttype' in kwargs:
                model = kwargs['contenttype']

            # ContentType
            self.target_content_type = ContentType.objects.get(model=model)

            # Model class
            self.target_model_class = self.target_content_type.model_class()

            # Model field
            if 'field_name' in kwargs:
                # TODO: Catch abuse of field lookups
                field = self.target_model_class._meta.get_field_by_name(kwargs['field_name'])[0]
                self.target_model_field_name = field.name

            # Model instance
            if 'model_pk' in kwargs:
                self.target_model_instance_pk = kwargs['model_pk']
            elif 'pk' in kwargs: # dispatch from embedded app urls
                self.target_model_instance_pk = kwargs['pk']
            if self.target_model_instance_pk is not None:
                self.target_model_instance = self.target_model_class.objects.get(
                        pk=self.target_model_instance_pk)

        # reports_fieldname = None
        # # Inspect the Report model's reverse relationships and find the field name being used on the target model. Typically this would be "reports", as in "MyModel.reports"
        # for rel, _model in self.model._meta.get_all_related_m2m_objects_with_model():
        #     if rel.model == model_class:
        #         reports_fieldname = rel.field.name
        #         break
        # else:
        #     # FIXME: This error can be raised by any client requesting a contenttype name that simply doesn't leverage the reports app.
        #     msg = "%r doesn't declare a relationship to %r" % (self.target_model_class, self.model)
        #     raise ValueError(msg)

    def get_queryset(self):
        queryset = self.model.objects.all()
        if self.target_content_type:
            queryset = queryset.filter(content_type=self.target_content_type)
            if self.target_model_field_name:
                queryset = queryset.filter(object_fieldname=self.target_model_field_name)
        return queryset

    def get_object(self):
        return self.target_model_instance

    def get_context_data(self, **kwargs):
        context = super(ReportMixin, self).get_context_data(**kwargs)
        if self.target_model_instance:
            context[self.target_model_class._meta.module_name] = self.target_model_instance
            context.update({
                'content_type': self.target_content_type,
                'model': self.target_model_class,
                'field_name': self.target_model_field_name,
                'instance': self.target_model_instance,
            })
        return context

    def get_template_names(self):
        template_names = [self.template_name]
        if self.target_model_class:
            template_names = [
                'reports/{}{}.html'.format(self.target_model_class._meta.module_name, self.template_name_suffix),
                '{}/report{}.html'.format(self.target_model_class._meta.module_name + 's', self.template_name_suffix),
            ] + template_names
        logger.error(template_names)
        return template_names

class ReportListView(ReportMixin, ListView):
    permissions_required = ['reports.change_report']
    template_name = 'reports/report_list.html'

    def get_context_data(self, **kwargs):
        context = super(ReportListView, self).get_context_data(**kwargs)
        context.update({
            'model': self.target_model_class.__name__ if self.target_model_class else None,
            'content_type': self.target_content_type,
            'instance': self.target_model_instance,
        })
        return context

class ReportDetailView(ReportMixin, DetailView):
    permissions_required = ['reports.change_report']
    template_name = 'reports/report_detail.html'


class ReportFormMixin(object):
    form_class = ReportForm
    template_name = 'reports/report_form.html'

    def get_initial(self):
        return {
            'content_type': self.target_content_type,
            'object_id': self.target_model_instance_pk,
            'object_fieldname': self.target_model_field_name,
        }

    def get_form_kwargs(self):
        kwargs = super(ReportFormMixin, self).get_form_kwargs()
        kwargs.update({
            'model': self.target_model_class,
        })
        return kwargs
    
class ReportCreateView(ReportMixin, ReportFormMixin, CreateView):
    # permissions_required = ['reports.add_report']
    pass

class ReportUpdateView(ReportMixin, ReportFormMixin, UpdateView):
    permissions_required = ['reports.change_report']
