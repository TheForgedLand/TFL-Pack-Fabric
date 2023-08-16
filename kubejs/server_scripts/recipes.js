
ServerEvents.recipes(event => {
	// Change recipes here
	event.remove({output: "expandeddelight:cheese_wheel"})

	event.replaceInput(
		{ input: "expandeddelight:cheese_slice" },
		"expandeddelight:cheese_slice",
		"brewinandchewin:flexan_cheese_wedge"
	)

})

console.info('Recipes reloaded!!')