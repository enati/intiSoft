# -*- coding: utf-8 -*-
from django import forms


class MultiSelectWidget(forms.widgets.SelectMultiple):

    def render(self, name, value, attrs=None):
        import pdb; pdb.set_trace()
        html = super(MultiSelectWidget, self).render(name, value, attrs)

        """
        '<select multiple="multiple" class="form-control " id="id_IEM" name="IEM">
            <option value="5">Galga</option>\n<option value="6">Tamices</option>
            <option value="7">Balanzas</option>\n<option value="8">Varios</option>
            <option value="9">Asistencia Tecnica</option>
        </select>'
        """
        html ="""<select multiple="multiple" class="form-control " id="id_IEM" name="IEM">
            <option value="5">Galga</option>
            <option value="6">Tamices</option>
        </select>"""
        #html = """
             #<script type="text/javascript">
               #var populatePRNotes = function() {
                 ## Use jQuery to select the fields that will
                 ## populate this field
                 #var qty = document
                                #.getElementById('id_qty').value;
                 #var item = document
                            #.getElementById('id_name').value;
                 #var who = document
                           #.getElementById('id_who').value;

                 ## Get the id of the purchase request
                 ## from the form
                 #var pr_id = document
                   #.getElementsByClassName('#field-request_id')
                   #.value;

                 ## Careful here: we're ending the string,
                 ## inserting the dictionary we built earlier,
                 ## and then continuing our string.
                 #var pr_asset_dict = """ +
                                     #str(pr_asset_dict) + """;

                 ## Now access the dictionary using the purchase
                 ## request id as a key to get the corresponding
                 ## asset (if there is one)
                 #var pr_asset = pr_asset_dict[pr_id];

                 ## Build the text to display in the form field.
                 #var display_text = qty + ' ' + item +
                                    #' for ' + who
                 #if (pr_asset) {
                   #display_text += ' (Asset #' + pr_asset + ')'
                 #}
                 #document.getElementById('id_accounting_memo')
                         #.innerHTML = display_text;
               #}
             #</script>
             #""" + html + """
             ## This button will trigger the script's function
             ## and fill in the field.
             #<button type="button" onclick="populatePRNotes()">
               #Create PR Notes
             #</button>
             #""";

        # Since we are using string concatenation, we need to
        # mark it as safe in order for it to be treated as
        # html code.
        return html