<h3>Lint</h3>
<div class="lint">
<table class="listing lint scroll" id="nosebitten_lint">
  <thead>
    <tr>
      <th>Type</th>
      <th>Class/File</th>
      <th>Line</th>
      <th>Message</th>
    </tr>
  </thead>
  <tbody style="overflow: auto; max-height: 40em; width: 100%; overflow-x: hidden;">
  <?cs each:item = data ?>
  <tr class="<?cs var:item.cat ?>">
    <td><?cs var:item.type ?></td>
    <td><a href="<?cs var:item.href ?>#L<?cs var:item.line ?>">
    <?cs if:item.tag ?><?cs var:item.tag ?><?cs else ?><?cs var:item.file ?><?cs /if ?></a></td>
    <td><?cs var:item.line ?></td>
    <td><?cs var:item.msg ?></td>
  </tr><?cs /each ?>
  </tbody>
</table>
</div>
<div id="sorting">
  <div>Sorting tables, please hold on...</div>
</div>
<script>
$(document).ready(function() {
    $("#nosebitten_lint").tableSorter({
        sortColumn: 'Class/File',         // Integer or String of the name of the column to sort by.
        sortClassAsc: 'sortUp',       // class name for ascending sorting action to header
        sortClassDesc: 'sortDown',    // class name for descending sorting action to header
        headerClass: 'largeHeaders',           // class name for headers (th's)
    });
    //$("table.nosebitten_lint").grid({height: 350, width: [150,150,150,150]});
});
</script>
