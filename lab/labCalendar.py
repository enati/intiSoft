# -*- coding: utf-8 -*-
from adm.views import Presupuesto, Usuario
from calendar import HTMLCalendar, month_name
from datetime import date
from itertools import groupby
from django.utils.html import conditional_escape as esc
from django.core.urlresolvers import reverse


class WorkoutCalendar(HTMLCalendar):

    def __init__(self, workouts, lab):
        super(WorkoutCalendar, self).__init__()
        self.workouts = self.group_by_day(workouts)
        self.lab = lab

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            cssstate = {'en_espera': 'neutral',
                        'activo': 'warning',
                        'finalizado': 'success',
                        'cancelado': 'danger'}
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.workouts:
                cssclass += ' filled'
                body = ['<ul class="list-unstyled">']
                for workout in self.workouts[day]:
                    if workout.presupuesto_id:
                        if workout.revisionar:
                            cssstate[workout.estado] += ' overlay2'
                        body.append('<li style="position: relative" class= "%s">' % cssstate[workout.estado])
                        body.append("<a href=" + reverse('lab:%s-update' % self.lab, kwargs={'pk': workout.id}) + ">")
                        presup_obj = Presupuesto.objects.get(pk=workout.presupuesto_id)
                        user_obj = Usuario.objects.get(pk=presup_obj.usuario_id)
                        body.append(esc(user_obj.nombre))
                        body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        self.year, self.month = theyear, themonth
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="table month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def formatmonthname(self, theyear, themonth, withyear=True):
        """
        Return a month name as a table row.
        """
        if withyear:
            s = '%s %s' % (month_name[themonth], theyear)
        else:
            s = '%s' % month_name[themonth]
        nextMonth, nextYear = self.next_month(themonth, theyear)
        previousMonth, previousYear = self.previous_month(themonth, theyear)
        if len(nextMonth) == 1:
            nextMonth = '0' + nextMonth
        if len(previousMonth) == 1:
            previousMonth = '0' + previousMonth
        return """<tr><th colspan="7" class="month">
                    <a href=""" + reverse('lab:%s-calendar' % self.lab, kwargs={'year': previousYear, 'month': previousMonth}) + """>
                        <span class="glyphicon glyphicon-menu-left" aria-hidden="true"></span>
                    </a>""" +\
                    s +\
                    """<a href=""" + reverse('lab:%s-calendar' % self.lab, kwargs={'year': nextYear, 'month': nextMonth}) + """>
                        <span class="glyphicon glyphicon-menu-right" aria-hidden="true"></span>
                    </a>
                </th></tr>"""

    def group_by_day(self, workouts):
        field = lambda workout: workout.fecha_inicio.day
        return dict(
            [(day, list(items)) for day, items in groupby(workouts, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

    def next_month(self, month, year):
        if month == 12:
            return ('1', str(year + 1))
        else:
            return (str(month + 1), str(year))

    def previous_month(self, month, year):
        if month == 1:
            return ('12', str(year - 1))
        else:
            return (str(month - 1), year)
