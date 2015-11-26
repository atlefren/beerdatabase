function doSomething ( values, handle, unencoded ) {
	// values: Current slider values;
	// handle: Handle that caused the event;
	// unencoded: Slider values without formatting;
}

// Binding signature
slider.noUiSlider.on(eventName, doSomething);

// Binding namespaced events
slider.noUiSlider.on('set.one', function(){});
slider.noUiSlider.on('change.one', function(){});

// Remove all events in the 'one' namespace.
slider.noUiSlider.off('.one');

// Remove all 'change' events in any namespace.
slider.noUiSlider.off('change');
