

$(document).ready(function(){

    $.ajax({
    type: 'POST',
    url: '/get_country',
    dataType: 'json',
    data : {},
    }).done(function(data){

        country_select= $('#select_country').empty();
        country_select_data= '<option value="" selected="selected">COUNTRY</option>';

        for(i=0;i<data.countries.length; i++){
            country_select_data+='<option value="'+data.countries[i].id+'">'+data.countries[i].value+'</option>'
        }

        country_select.append(country_select_data)


    });



    $.ajax({
    type: 'POST',
    url: '/get_year',
    dataType: 'json',
    data : {},
    }).done(function(data){
        load_year=$('#age_year').empty();
        load_year_data='<option value="" selected="selected">YEAR</option>';

        load_month=$('#age_month').empty();
        load_month_data='<option value="" selected="selected">MONTH</option>';

        load_days=$('#age_day').empty();
        load_days_data='<option value="" selected="selected">DAYS</option>';

        $.each(data.year, function( index, value ) {
             if (index >= 0) {
                load_year_data+='<option value="'+value+'">'+value+'</option>'
            }
        });
        load_year.append(load_year_data)

        $.each(data.months, function( index, value ) {
             if (index >= 0) {
                load_month_data+='<option value="'+value+'">'+value+'</option>'
            }
        });
        load_month.append(load_month_data)

        $.each(data.days, function( index, value ) {
             if (index >= 0) {
                load_days_data+='<option value="'+value+'">'+value+'</option>'
            }
        });
        load_days.append(load_days_data)


    });

});


