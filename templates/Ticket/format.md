<div ng-controller="TicketCtrl">
    <div class="content-wrapper">
        <div class="content-header">
            <div class="container-fluid">
                <div class="row mb-2">
                    <div class="col-sm-12">
                    </div>
                </div>
            </div>
        </div>
        {% include 'partial/_flashbag.twig' %}
        <div class="content">
            <div class="container-fluid">
                <div class="row rtl">
                    <div class="col-sm-12 col-md-12">
                        <div class="card card-primary card-outline">
                            <div class="card-header">
                                تمام تیکت‌ها
                            </div>
                            <div class="card-body">
                                <table class="table table-bordered">
                                    <thead>
                                        <tr>
                                            <th style="background-color: #1e1235; color: white;" class="text-center">آمار تیکت‌ها</th>
                                            {% for item in status %}
                                                <th style="border-top: 5px solid {{ item.color }};" class="text-center">{{ item.name }}</th>
                                            {% endfor %}
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% width = (100-16)/(status|length) %}
                                        {% for item in category %}
                                            <tr>
                                                <td class="text-left">{{ item.name }}</td>
                                                {% for item_status in status %}
                                                    {% id = item.ticket_system_category_id ~ '_' ~ item_status.ticket_system_status_id %}
                                                    {% if row[id]['cnt'] is defined and row[id]['cnt'] != 0 %}
                                                        <td style="width: {{ width }}%; background-color: #fafafa;" class="text-center">
                                                            <a href="{{ path('ticket.all.view', {'report': 'category', 'id': item.ticket_system_category_id, 'status_id': item_status.ticket_system_status_id}) }}">
                                                                {{ row[id]['cnt'] }}
                                                            </a>
                                                        </td>
                                                    {% else %}
                                                        <td style="width: {{ width }}%" class="text-center">-</td>
                                                    {% endif %}
                                                {% endfor %}
                                            </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                            
                        </div>
                        <div class="card card-primary card-outline">
                            <div class="card-header">
                                انجام دهندگان تیکت‌ها
                            </div>
                            <div class="card-body">
                                <table class="table table-bordered">
                                    <thead>
                                        <tr>
                                            <th colspan="2" style="background-color: #1e1235; color: white;" class="text-center">آمار تیکت‌ها</th>
                                            {% for item in status %}
                                                <th style="border-top: 5px solid {{ item.color }};" class="text-center">{{ item.name }}</th>
                                            {% endfor %}
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% width = (100-16)/(status|length) %}
                                        {% for item in user %}
                                            <tr>
                                                <td rowspan="4" class="text-left">{{ item.name }}</td>
                                            </tr>
                                            <tr>
                                                <td class="text-left">انجام دهنده</td>
                                                {% for item_status in status %}
                                                    {% id = item.user_id ~ '_' ~ item_status.ticket_system_status_id %}
                                                    {% if rowDoer[id]['cnt'] is defined and rowDoer[id]['cnt'] != 0 %}
                                                        <td style="width: {{ width }}%; background-color: #fafafa;" class="text-center">
                                                            <a href="{{ path('ticket.all.view', {'report': 'doer', 'id': item.user_id, 'status_id': item_status.ticket_system_status_id}) }}">
                                                                {{ rowDoer[id]['cnt'] }}
                                                            </a>
                                                        </td>
                                                    {% else %}
                                                        <td style="width: {{ width }}%" class="text-center">-</td>
                                                    {% endif %}
                                                {% endfor %}
                                            </tr>
                                            <tr>
                                                <td class="text-left">همکار</td>
                                                {% for item_status in status %}
                                                    {% id = item.user_id ~ '_' ~ item_status.ticket_system_status_id %}
                                                    {% if rowColleg[id]['cnt'] is defined and rowColleg[id]['cnt'] != 0 %}
                                                        <td style="width: {{ width }}%; background-color: #fafafa;" class="text-center">
                                                            <a href="{{ path('ticket.all.view', {'report': 'coworker', 'id': item.user_id, 'status_id': item_status.ticket_system_status_id}) }}">
                                                                {{ rowColleg[id]['cnt'] }}
                                                            </a>
                                                        </td>
                                                    {% else %}
                                                        <td style="width: {{ width }}%" class="text-center">-</td>
                                                    {% endif %}
                                                {% endfor %}
                                            </tr>
                                            <tr style="border-bottom: 3px solid black;">
                                                <td class="text-left">مشاهده</td>
                                                {% for item_status in status %}
                                                    {% id = item.user_id ~ '_' ~ item_status.ticket_system_status_id %}
                                                    {% if rowViewer[id]['cnt'] is defined and rowViewer[id]['cnt'] != 0 %}
                                                        <td style="width: {{ width }}%; background-color: #fafafa;" class="text-center">
                                                            <a href="{{ path('ticket.all.view', {'report': 'view', 'id': item.user_id, 'status_id': item_status.ticket_system_status_id}) }}">
                                                                {{ rowViewer[id]['cnt'] }}
                                                            </a>
                                                        </td>
                                                    {% else %}
                                                        <td style="width: {{ width }}%" class="text-center">-</td>
                                                    {% endif %}
                                                {% endfor %}
                                            </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                        </div><!-- /card card-primary card-outline -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>