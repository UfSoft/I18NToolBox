<h3>Code Coverage</h3>
<table class="listing coverage" id="nosebitten_coverage">
 <thead><!--
   <tr>
     <th class="name">Unit</th>
     <th class="loc">Lines of Code</th>
     <th class="exe">Executed Lines</td>
     <th class="cov">Coverage</th>
     <th class="missed">Missed Lines</th>
   </tr> -->
   <tr>
     <th>Unit</th>
     <th>Lines of Code</th>
     <th>Executed Lines</td>
     <th>Coverage</th>
     <th>Missed Lines</th>
   </tr>
 </thead>
 <tbody><?cs
 each:item = data ?>
  <tr>
    <td class="name">
      <?cs if:item.href ?><a href="<?cs var:item.href ?>"><?cs var:item.name ?></a>
      <?cs else ?><?cs var:item.name ?>
      <?cs /if ?>
    </td>
    <td class="loc"><?cs var:item.loc ?></td>
    <td class="exec"><?cs var:item.exe ?></td>
    <td class="cov"><?cs var:item.cov ?>%</td>
    <td class="miss">
    <?cs each:missed = item.miss ?>
      <?cs if:missed.href ?><a href="<?cs var:missed.href ?>"><?cs var:missed.lines ?></a>
      <?cs else ?><?cs var:missed.lines ?>
      <?cs /if ?>
    <?cs /each ?>
    </td>
  </tr><?cs /each ?>
 </tbody>
 <tbody class="totals">
   <tr>
     <th>Total</th>
     <td><?cs var:totals.loc ?></td>
     <td><?cs var:totals.exe ?></td>
     <td><?cs var:totals.cov ?>%</td>
     <td> </td>
   </tr>
 </tbody>
</table>
<div id="sorting">
  <div>Sorting tables, please hold on...</div>
</div>
<script>
$(document).ready(function() {
    $("#nosebitten_coverage").tableSorter({
        sortColumn: 'Unit',         // Integer or String of the name of the column to sort by.
        sortClassAsc: 'sortUp',       // class name for ascending sorting action to header
        sortClassDesc: 'sortDown',    // class name for descending sorting action to header
        headerClass: 'largeHeaders',           // class name for headers (th's)
        disableHeader: ['Missed Lines'],
    });
});
</script>
