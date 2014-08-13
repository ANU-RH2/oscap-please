<%!
    ## python module-level code
    import datetime
    import fakedata

    ## python code block
    def getDate():
        return datetime.datetime.now()

    data = fakedata.get_MVP()

    resultcount = {}
    for i in data:
      if i['result'] in resultcount:
        resultcount[i['result']] = resultcount[i['result']] + 1
      else:
        resultcount[i['result']] = 1

    resultcolours = {'fail': '#FE6A6A',
                     'error': '#997D65',
                     'notapplicable': '#EAD376',
                     'notselected': '#CCCCCC',
                     'pass': '#A6EAAA',
                     'fixed': '#B0CFFE'}
%>

<%def name="makerowx(i)">
    <tr>
        <td class=${i['result']}>${i['result']}</td>\
        <td>${i['machine_name']}</td>\
        <td>${i['date'].isoformat()}</td>\
    </tr>
</%def>

<html>
 <head>
         <link rel="stylesheet" type="text/css" href="style.css">
         <script src="sorttable.js"></script>
         <script src="Chart.js"></script>
         <script type="text/javascript">
            function createChart() {
                var data = [

                % for i in resultcount:
                    {
                      value: ${resultcount[i]},
                      color:"${resultcolours[i]}",
                      ##highlight: "#FF5A5E",
                      label: "${i}"
                    },
                % endfor

                ];
                    var cht = document.getElementById('trChart');
                    var ctx = cht.getContext('2d');
                    var barChart = new Chart(ctx).Pie(data);
                }
         </script>
 </head>
 <body onload="createChart();">

    <h1>OSP Report</h1>
    <h3>Generated at ${getDate()}</h2>

    <br>

    <div class="left">
        <table class="sortable" id="report_table">
            <thead>
                <tr>
                   <th>Result</th>
                   <th>Machine Name</th>
                   <th>Date</th>
                </tr>
            </thead>
            <tbody>
                <%
                   for i in data:
                    ##if i['result'] == 'fail':
                     {makerowx(i)}
                    ##endif
                   endfor
                %>
            <tbody>
        </table>
    </div>

    <div class="right">
         <center>
            <canvas id="trChart" width="1000" height="700"></canvas>
         </center>
    </div>
 </body>
</html>