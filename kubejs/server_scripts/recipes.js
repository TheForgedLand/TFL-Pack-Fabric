
ServerEvents.recipes(event => {
	// Change recipes here

	event.remove({input: "create:dough"})
	event.replaceOutput(
		{ output: "create:dough" },
		"create:dough",
		"farmersdelight:wheat_dough"
	)

	event.replaceInput(
		{id: "minecraft:writable_book"},
		"minecraft:ink_sac",
		"minecraft:black_dye"
	)
	event.smelting("minecraft:leather", "minecraft:rotten_flesh")

	event.remove({ id: "minecraft:chain" })
	event.remove({ id: "architects_palette:nether_brass_chain" })
	let chain = (id, metal_id) => {
		event.shaped(
			Item.of(id,4), [
			'N',
			'I',
			'N'
		], {
			N: metal_id + '_nugget',
			I: metal_id + '_ingot',
		})
	}
	chain("minecraft:chain", "minecraft:iron")
	chain("architects_palette:nether_brass_chain", "architects_palette:nether_brass")


	event.remove({ output: "expandeddelight:cheese_wheel" })
	event.replaceInput(
		{ input: "expandeddelight:cheese_slice" },
		"expandeddelight:cheese_slice",
		"brewinandchewin:flexan_cheese_wedge"
	)



})

console.info('Recipes reloaded!!')