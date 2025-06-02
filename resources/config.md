Sky's Jouzu BulkOps (Config)
---

### Unpack

- `field_dictionary`: The name of the field containing the dictionary's output.
- `field_reading`: The name of the field where to store the extracted reading.
- `tag_fail`: The tag to add to the note if the unpacking operation fails.'

### Pitch

- `field_reading`: The name of the field containing the pitch accent graph.
- `fields_tocolour`: The list of the fields to colour. A list is a sequence of values separated by commas and enclosed in square brackets.
- `colour_heiban`: The colour of heiban words.
- `colour_atamadaka`: The colour of atamadaka words.
- `colour_nakadaka`: The colour of nakadaka words.
- `colour_oodaka`: The colour of oodaka words.
- `tag_fail`: The tag to add to the note if the colouring operation fails.
- `colour_graph`: `true` to colour the pitch graph too, `false` otherwise.

The colours can be in any css format, such as `red`, `#ff0000`, `rgb(255, 0, 0)`.
