from __future__ import annotations
from enum import Enum
from arcgis.map._dataclasses._webmap_spec import BaseModel, common_config
from typing import Annotated, Any, Optional, Literal, Union
from pydantic import Field
from arcgis.auth.tools import LazyLoader

_map = LazyLoader("arcgis.map.map_widget")
_scene = LazyLoader("arcgis.map.scene_widget")
_group = LazyLoader("arcgis.map.group_layer")


class ArcadeReturnType(Enum):
    """
    Return type of the Arcade expression, can be a number or string.
    Number values are assumed to be `double`.
    Knowing the `ArcadeReturnType` allows the authoring client to present
    fields in relevant contexts. For example, numeric fields in numeric
    contexts such as chart values.
    """

    number = "number"
    string = "string"


class DateFormat(Enum):
    """
    A string used with date fields to specify how the date should be formatted.
    """

    day_short_month_year = "dayShortMonthYear"
    day_short_month_year_long_time = "dayShortMonthYearLongTime"
    day_short_month_year_long_time24 = "dayShortMonthYearLongTime24"
    day_short_month_year_short_time = "dayShortMonthYearShortTime"
    day_short_month_year_short_time24 = "dayShortMonthYearShortTime24"
    long_date = "longDate"
    long_date_long_time = "longDateLongTime"
    long_date_long_time24 = "longDateLongTime24"
    long_date_short_time = "longDateShortTime"
    long_date_short_time24 = "longDateShortTime24"
    long_month_day_year = "longMonthDayYear"
    long_month_day_year_long_time = "longMonthDayYearLongTime"
    long_month_day_year_long_time24 = "longMonthDayYearLongTime24"
    long_month_day_year_short_time = "longMonthDayYearShortTime"
    long_month_day_year_short_time24 = "longMonthDayYearShortTime24"
    long_month_year = "longMonthYear"
    short_date = "shortDate"
    short_date_le = "shortDateLE"
    short_date_le_long_time = "shortDateLELongTime"
    short_date_le_long_time24 = "shortDateLELongTime24"
    short_date_le_short_time = "shortDateLEShortTime"
    short_date_le_short_time24 = "shortDateLEShortTime24"
    short_date_long_time = "shortDateLongTime"
    short_date_long_time24 = "shortDateLongTime24"
    short_date_short_time = "shortDateShortTime"
    short_date_short_time24 = "shortDateShortTime24"
    short_month_year = "shortMonthYear"
    year = "year"


class StatisticType(Enum):
    """
    Used in a 1:many or many:many relationship to compute the statistics on
    the field to show in the popup.
    """

    avg = "avg"
    count = "count"
    max = "max"
    min = "min"
    stddev = "stddev"
    sum = "sum"
    var = "var"


class StringFieldOption(Enum):
    """
    A string determining what type of input box editors see when editing the
    field. Applies only to string fields. Not applicable to Arcade expressions.
    """

    richtext = "richtext"
    textarea = "textarea"
    textbox = "textbox"


class MediaType(Enum):
    """
    A string defining the type of media.
    """

    barchart = "barchart"
    columnchart = "columnchart"
    image = "image"
    linechart = "linechart"
    piechart = "piechart"


class AttachmentDisplayType(Enum):
    """
    This property applies to elements of type `attachments`. A string value
    indicating how to display the attachment. If `list` is specified, attachments
    show as links. If `preview` is specified, attachments expand to the width of
    the pop-up. The default `auto` setting allows applications to choose the most
    suitable default experience.
    """

    auto = "auto"
    list = "list"
    preview = "preview"


class Order(Enum):
    """
    Indicates whether features are sorted in ascending or descending order of
    the field values.
    """

    asc = "asc"
    desc = "desc"


class Format(BaseModel):
    """
    The format object can be used with numerical or date fields to provide
    more detail about how values should be formatted for display.
    """

    model_config = common_config

    date_format: Optional[DateFormat] = Field(
        None,
        alias="dateFormat",
        description="A string used with date fields to specify how the date should be formatted.",
    )
    digit_separator: Optional[bool] = Field(
        None,
        alias="digitSeparator",
        description="A Boolean used with numerical fields. If True, allows the number to have a digit (or thousands) separator. Depending on the locale, this separator is a decimal point or a comma. If False, means that no separator will be used.",
    )
    places: Optional[int] = Field(
        None,
        description="An integer used with numerical fields to specify the number of decimal places. Any places beyond this value are rounded.",
    )


class FieldInfo(BaseModel):
    """
    Defines how a field in the dataset participates (or does not participate) in a popup window.
    """

    model_config = common_config

    field_name: Optional[str] = Field(
        None,
        alias="fieldName",
        description="A string containing the field name as defined by the service.",
    )
    format: Optional[Format] = Field(
        None,
        description="A format object used with numerical or date fields to provide more detail about how the value should be displayed in a web map popup window.",
    )
    is_editable: Optional[bool] = Field(
        True,
        alias="isEditable",
        description="A Boolean determining whether users can edit this field. Not applicable to Arcade expressions.",
    )
    label: Optional[str] = Field(
        None,
        description="A string containing the field alias. This can be overridden by the web map author. Not applicable to Arcade expressions as `title` is used instead.",
    )
    statistic_type: Optional[StatisticType] = Field(
        None,
        alias="statisticType",
        description="Used in a 1:many or many:many relationship to compute the statistics on the field to show in the popup.",
    )
    string_field_option: Optional[StringFieldOption] = Field(
        None,
        alias="stringFieldOption",
        description="A string determining what type of input box editors see when editing the field. Applies only to string fields. Not applicable to Arcade expressions.",
    )
    tooltip: Optional[str] = Field(
        None,
        description="A string providing an editing hint for editors of the field. Not applicable to Arcade expressions.",
    )
    visible: Optional[bool] = Field(
        None,
        description="A Boolean determining whether the field is visible in the popup window.",
    )


class LayerOptions(BaseModel):
    """
    Additional options available for the popup layer.
    """

    model_config = common_config

    return_topmost_raster: Optional[bool] = Field(
        None,
        alias="returnTopmostRaster",
        description="Indicates whether or not only the topmost raster should be displayed.",
    )
    show_no_data_records: Optional[bool] = Field(
        None,
        alias="showNoDataRecords",
        description="Indicates whether or not the NoData records should be displayed.",
    )


class Value(BaseModel):
    """
    The value object contains information for popup windows about how images should be retrieved or charts constructed.
    """

    model_config = common_config

    colors: Optional[list[list[Annotated[int, Field(ge=0, le=255)]]]] = Field(
        None,
        description="Used with charts. An optional array of colors where each `color` sequentially corresponds to a field in the `fields` property. When the value for `mediaInfo.type` is `linechart`, the first color in the array will drive the line color. If `colors` is longer than `fields`, unmatched colors are ignored. If `colors` is shorter than `fields` or `colors` isn't specified, a default color ramp is applied.",
    )
    fields: Optional[list[str]] = Field(
        None,
        description="Used with charts. An array of strings, with each string containing the name of a field to display in the chart.",
    )
    link_url: Optional[str] = Field(
        None,
        alias="linkURL",
        description="Used with images. A string containing a URL to be launched in a browser when a user clicks the image.",
    )
    normalize_field: Optional[str] = Field(
        None,
        alias="normalizeField",
        description="Used with charts. An optional string containing the name of a field. The values of all fields in the chart will be normalized (divided) by the value of this field.",
    )
    source_url: Optional[str] = Field(
        None,
        alias="sourceURL",
        description="Used with images. A string containing the URL to the image.",
    )
    tooltip_field: Optional[str] = Field(
        None,
        alias="tooltipField",
        description="String value indicating the tooltip for a chart specified from another field. This field is needed when related records are not used. It is used for showing tooltips from another field in the same layer or related layer/table.",
    )


class MediaInfo(BaseModel):
    """
    Defines an image or a chart to be displayed in a popup window.
    """

    model_config = common_config

    alt_text: Optional[str] = Field(
        None,
        alias="altText",
        description="A string providing the alternate text for the media.",
    )
    caption: Optional[str] = Field(
        None, description="A string caption describing the media."
    )
    refresh_interval: Optional[Union[float, int]] = Field(
        0,
        alias="refreshInterval",
        description="Refresh interval of the layer in minutes. Non-zero value indicates automatic layer refresh at the specified interval. Value of 0 indicates auto refresh is not enabled. If the property does not exist, it's equivalent to having a value of 0. Only applicable when `type` is set to `image`.",
    )
    title: Optional[str] = Field(None, description="A string title for the media.")
    type: Optional[MediaType] = Field(
        None, description="A string defining the type of media."
    )
    value: Optional[Value] = Field(
        None,
        description="A value object containing information about how the image should be retrieved or how the chart should be constructed.",
    )


class PopupElementAttachments(BaseModel):
    """
    Configures attachments in popup elements.
    """

    model_config = common_config

    description: Optional[str] = Field(
        None, description="An optional string value describing the element in detail."
    )
    display_type: Optional[AttachmentDisplayType] = Field(
        None,
        alias="displayType",
        description="This property applies to elements of type `attachments`. A string value indicating how to display the attachment. If `list` is specified, attachments show as links. If `preview` is specified, attachments expand to the width of the pop-up. The default `auto` setting allows applications to choose the most suitable default experience.",
    )
    title: Optional[str] = Field(
        None,
        description="An optional string value indicating what the element represents.",
    )
    type: Literal["attachments"] = "attachments"


class PopupExpressionInfo(BaseModel):
    """
    An Arcade expression that defines the pop-up element content. The return type will always be a `dictionary` that defines the desired pop-up element as outlined [in the Arcade documentation](https://developers.arcgis.com/arcade/guide/profiles/#popup-element).
    """

    model_config = common_config

    expression: str = Field(..., description="The Arcade expression.")
    return_type: Optional[ArcadeReturnType] = Field(
        "string",
        alias="returnType",
        description="Optional return type of the Arcade expression. Defaults to string value. Number values are assumed to be `double`. This can be determined by the authoring client by executing the expression using a sample feature, although it can be corrected by the user. Knowing the returnType allows the authoring client to present fields in relevant contexts. For example, numeric fields in numeric contexts such as charts.",
    )
    title: Optional[str] = Field(None, description="Title of the expression.")


class PopupElementFields(BaseModel):
    """
    Configures fields in popup elements.
    """

    model_config = common_config

    attributes: Optional[dict[str, Any]] = Field(
        None,
        description="A dictionary of key value pairs representing attributes to be used instead of fields and their values. This property is only used when an element of type `fields` is being returned inside an element of type `expression` and should be returned as part of the arcade expression itself. This property allows passing arcade derived attribute values into `fields` elements. More details can be found [here](https://developers.arcgis.com/arcade/guide/profiles/#popup-element).",
    )
    description: Optional[str] = Field(
        None, description="An optional string value describing the element in detail."
    )
    field_infos: Optional[list[FieldInfo]] = Field(
        None,
        alias="fieldInfos",
        description="It is an array of `fieldInfo` objects representing a field/value pair displayed as a table within the popupElement. If the `fieldInfos` property is not provided, the popupElement will display whatever is specified directly in the `popupInfo.fieldInfos` property.",
    )
    title: Optional[str] = Field(
        None,
        description="An optional string value indicating what the element represents.",
    )
    type: Literal["fields"] = Field(
        "fields", description="Specifies the type of element."
    )


class PopupElementMedia(BaseModel):
    """
    Configures media in popup elements.
    """

    model_config = common_config

    attributes: Optional[dict[str, Any]] = Field(
        None,
        description="A dictionary of key value pairs representing attributes to be used instead of fields and their values.  This property is only used when an element of type  `media` is being returned inside an element of type `expression` and should be returned as part of the arcade expression itself. This property allows passing arcade derived attribute values into `mediaInfos` such as charts. More details can be found [here](https://developers.arcgis.com/arcade/guide/profiles/#popup-element).",
    )
    description: Optional[str] = Field(
        None, description="An optional string value describing the element in detail."
    )
    media_infos: Optional[list[MediaInfo]] = Field(
        None,
        alias="mediaInfos",
        description="An array of `mediaInfo` objects representing an image or chart for display. If no `mediaInfos` property is provided, the popupElement will display whatever is specified in the `popupInfo.mediaInfos` property.",
    )
    title: Optional[str] = Field(
        None,
        description="An optional string value indicating what the element represents.",
    )
    type: Literal["media"] = "media"


class OrderByField(BaseModel):
    """
    Object defining the display order of features or records based on a field value, and whether they should be sorted in ascending or descending order.
    """

    model_config = common_config

    field: str = Field(
        ...,
        description="Name of a field. The value of this field will drive the sorting.",
    )
    order: Order = Field(
        ...,
        description="Indicates whether features are sorted in ascending or descending order of the field values.",
    )


class PopupElementRelationship(BaseModel):
    """
    Provides the ability to navigate and view related records from a layer or table associated within the popup.
    """

    model_config = common_config

    description: Optional[str] = Field(
        None, description="A string that describes the element in detail."
    )
    display_count: Optional[int] = Field(
        None,
        alias="displayCount",
        description="An integer that indicates the maximum number of records to display.",
    )
    display_type: Literal["list"] = Field(
        "list",
        alias="displayType",
        description="A string that defines how the related records should be displayed.",
    )
    order_by_fields: Optional[list[OrderByField]] = Field(
        None,
        alias="orderByFields",
        description="Array of `orderByField` objects indicating the display order for the related records, and whether they should be sorted in ascending `'asc'` or descending `'desc'` order. If `orderByFields` is not provided, the popupElement will display whatever is specified directly in the `popupInfo.relatedRecordsInfo.orderByFields` property.",
    )
    relationship_id: int = Field(
        ...,
        alias="relationshipId",
        description="The id of the relationship as defined in the feature layer definition",
    )
    title: Optional[str] = Field(
        None, description="A string value indicating what the element represents."
    )
    type: Literal["relationship"] = Field(
        "relationship",
        description="String value indicating which type of element to use.",
    )


class PopupElementText(BaseModel):
    """
    Configures text in popup elements.
    """

    model_config = common_config

    text: Optional[str] = Field(
        None,
        description="String value indicating the text to be displayed within the popupElement. If no `text` property is provided, the popupElement will display whatever is set in the popupInfo.description property.",
    )
    type: Literal["text"] = "text"


class RelatedRecordsInfo(BaseModel):
    """
    Applicable only when popupInfo contains a relationship content element. This is needed for backward compatibility for some web maps.
    """

    model_config = common_config

    order_by_fields: Optional[list[OrderByField]] = Field(
        None,
        alias="orderByFields",
        description="Array of orderByField objects indicating the field display order for the related records, and whether they should be sorted in ascending (asc) or descending (desc) order.",
    )
    show_related_records: Optional[bool] = Field(
        None,
        alias="showRelatedRecords",
        description="Required boolean value indicating whether to display related records. If True, client should let the user navigate to the related records. Defaults to True if the layer participates in a relationship AND the related layer/table has already been added to the map (either as an operationalLayer or as a table).",
    )


class PopupElementExpression(BaseModel):
    """
    A pop-up element defined by an arcade expression.
    """

    model_config = common_config

    expression_info: PopupExpressionInfo = Field(
        ...,
        alias="expressionInfo",
        description="An Arcade expression that defines the pop-up element content. The return type will always be `dictionary` as outlined [in the Arcade documentation](https://developers.arcgis.com/arcade/guide/profiles/#popup-element).",
    )
    type: Literal["expression"] = Field(
        "expression", description="Specifies the type of element."
    )


class AssociationType(Enum):
    connectivity = "connectivity"
    containment = "containment"
    structural = "structural"


class PopupElementUtilityNetworkAssociations(BaseModel):
    """
    Provides the ability to navigate and view associated objects from a layer or table associated within the [pop-up](popupInfo.md).
    """

    model_config = common_config

    associated_asset_group: int | None = Field(
        None,
        alias="associatedAssetGroup",
        description="The id of the asset group to filter utility network associations.",
    )
    associated_asset_type: int | None = Field(
        None,
        alias="associatedAssetType",
        description="The id of the asset type to filter utility network associations.",
    )
    associations_type: AssociationType | None = Field(
        ...,
        alias="associationsType",
        description="String value indicating which type of utility network associations to use.",
    )
    description: str | None = Field(
        None,
        description="A string that describes the element in detail.",
    )
    display_count: int | None = Field(
        None,
        alias="displayCount",
        description="An integer that indicates the maximum number of records to display.",
    )
    order_by_fields: list[OrderByField] | None = Field(
        None,
        alias="orderByFields",
        description="Array of `orderByField` objects indicating the display order for the related records, and whether they should be sorted in ascending `'asc'` or descending `'desc'` order. If `orderByFields` is not provided, the popupElement will display whatever is specified directly in the `popupInfo.relatedRecordsInfo.orderByFields` property.",
    )
    title: str | None = Field(
        None,
        description="A string value indicating what the element represents.",
    )
    type: Literal["utilityNetworkAssociations"] = Field(
        "utilityNetworkAssociations",
        description="String value indicating which type of element to use.",
    )


class PopupInfo(BaseModel):
    """
    Defines the look and feel of popup windows when a user clicks or queries a feature.
    """

    model_config = common_config

    description: Optional[str] = Field(
        None,
        description="A string that appears in the body of the popup window as a description. A basic subset of HTML may also be used to enrich the text. The supported HTML for ArcGIS Online can be seen in the [Supported HTML](https://doc.arcgis.com/en/arcgis-online/reference/supported-html.htm) page.",
    )
    expression_infos: Optional[list[PopupExpressionInfo]] = Field(
        None,
        alias="expressionInfos",
        description="List of Arcade expressions added to the pop-up.",
    )
    field_infos: Optional[list[FieldInfo]] = Field(
        None,
        alias="fieldInfos",
        description="Array of FieldInfo information properties. This information is provided by the service layer definition. When the description uses name/value pairs, the order of the array is how the fields display in the editable Map Viewer popup and the resulting popup. It is also possible to specify HTML-formatted content.",
    )
    layer_options: Optional[LayerOptions] = Field(
        None,
        alias="layerOptions",
        description="Additional options that can be defined for the popup layer.",
    )
    media_infos: Optional[list[MediaInfo]] = Field(
        None,
        alias="mediaInfos",
        description="Array of various mediaInfo to display. Can be of type `image`, `piechart`, `barchart`, `columnchart`, or `linechart`. The order given is the order in which is displays.",
    )
    popup_elements: Optional[
        list[
            Union[
                PopupElementAttachments,
                PopupElementExpression,
                PopupElementFields,
                PopupElementMedia,
                PopupElementRelationship,
                PopupElementText,
                PopupElementUtilityNetworkAssociations,
            ]
        ]
    ] = Field(
        None,
        alias="popupElements",
        description="An array of popupElement objects that represent an ordered list of popup elements.",
    )
    related_records_info: Optional[RelatedRecordsInfo] = Field(
        None,
        alias="relatedRecordsInfo",
        description="Applicable only when the pop-up contains a relationship content element. This is needed for backward compatibility for some web maps.",
    )
    show_attachments: Optional[bool] = Field(
        None,
        alias="showAttachments",
        description="Indicates whether attachments will be loaded for feature layers that have attachments.",
    )
    show_last_edit_info: Optional[bool] = Field(
        True,
        alias="showLastEditInfo",
        description="Indicates whether popup will display information about when and who last edited the feature. Applicable only to layers that have been configured to keep track of such information.",
    )
    title: Optional[str] = Field(
        None,
        description="A string that appears at the top of the popup window as a title.",
    )


class PopupManager:
    """
    A class that defines the popup found on a layer.
    Through this class you can edit the popup and get information on it.


    .. note::
        This class should not be created by a user but rather called through the `popup` method on
        a MapContent or GroupLayer instance.
    """

    def __init__(
        self,
        **kwargs: dict[str, Any],
    ) -> None:
        # The pydantic layer or table, this hooks it to the main webmap and tracks changes made
        self._layer = kwargs.pop("layer")
        self._spec = kwargs.pop("spec")
        self._parent = kwargs.pop("source")  # need to know where to find the layer
        self._source = (
            self._parent._source
        )  # need to know to update the correct dataclass
        self._is_table = kwargs.pop("is_table", False)

    def __str__(self) -> str:
        return "PopupManager for: " + self._layer.title

    def __repr__(self) -> str:
        return "PopupManager for: " + self._layer.title

    @property
    def info(self) -> PopupInfo | None:
        """
        Return the popup info for your layer. If no popup info
        is present then the value is None.

        Set the popup info for your layer.

        =====================       ===================================================================
        **Parameter**                **Definition**
        ---------------------       -------------------------------------------------------------------
        value                       Required PopupInfo object. The new popup info for the layer.
        =====================       ===================================================================
        """
        if self._layer.popup_info:
            # Pass into class here so if users want to edit it will show correct version
            return PopupInfo(**self._layer.popup_info.dict())
        else:
            return None

    @info.setter
    def info(self, info):
        if isinstance(self._parent, _map.MapContent):

            if self._is_table:
                # Update the main webmap dataclass in the MapContent
                for i, lyr in enumerate(self._parent._map._webmap.tables):
                    if lyr == self._layer:
                        self._parent._map._webmap.tables[i].popup_info = info
            else:
                # Update the main webmap dataclass in the MapContent
                for i, lyr in enumerate(self._parent._map._webmap.operational_layers):
                    if lyr == self._layer:
                        self._parent._map._webmap.operational_layers[i].popup_info = (
                            info
                        )
        elif isinstance(self._parent, _scene.SceneContent):
            if self._is_table:
                # Update the main webmap dataclass in the MapContent
                for i, lyr in enumerate(self._parent._scene._webscene.tables):
                    if lyr == self._layer:
                        self._parent._scene._webscene.tables[i].popup_info = info
            else:
                # Update the main webmap dataclass in the MapContent
                for i, lyr in enumerate(
                    self._parent._scene._webscene.operational_layers
                ):
                    if lyr == self._layer:
                        self._parent._scene._webscene.operational_layers[
                            i
                        ].popup_info = info
        elif isinstance(self._parent, _group.GroupLayer):
            # Update the layer in the group layer
            for i, lyr in enumerate(self._parent.layers):
                if lyr == self._layer:
                    self._parent.layers[i].popup_info = info
        self._layer.popup_info = info
        self._source._update_source()

    @property
    def title(self) -> str | None:
        """
        The title of the popup. If no title is present then the value is None.

        Set the title of the popup in the edit method.
        """
        if self._layer.popup_info:
            return self._layer.popup_info.title
        else:
            return None

    @property
    def disable_popup(self) -> bool:
        """
        Determine whether the popup is enabled for the layer, meaning it is visible when the map is rendered.

        Set whether the popup is enabled for the layer.

        =====================       ===================================================================
        **Parameter**                **Definition**
        ---------------------       -------------------------------------------------------------------
        value                       Required bool. Whether the popup is enabled for the layer.
        =====================       ===================================================================
        """
        return self._layer.disable_popup

    @disable_popup.setter
    def disable_popup(self, value: bool):
        self._layer.disable_popup = value
        self._source._update_source()

    def edit(
        self,
        title: str | None = None,
        description: str | None = None,
        expression_infos: list[PopupExpressionInfo] | None = None,
        field_infos: list[FieldInfo] | None = None,
        layer_options: LayerOptions | None = None,
        media_infos: list[MediaInfo] | None = None,
        popup_elements: (
            list[
                PopupElementAttachments
                | PopupElementExpression
                | PopupElementFields
                | PopupElementMedia
                | PopupElementRelationship
                | PopupElementText
            ]
            | None
        ) = None,
        show_attachments: bool | None = None,
    ) -> bool:
        """
        Edit the properties of the popup. If no popup info exists then it will create a popup for the layer.
        To remove any existing items from the popup, pass in an empty instance of the parameter. For example to
        remove the title, pass an empty string or to remove the field_infos pass an empty list. If the parameter
        is set to None then nothing will change for that parameter.

        =====================       ===================================================================
        **Parameter**                **Definition**
        ---------------------       -------------------------------------------------------------------
        title                       Optional string. Appears at the top of the popup window as a title.
        ---------------------       -------------------------------------------------------------------
        description                 Optional string. Appears in the body of the popup window as a description.
        ---------------------       -------------------------------------------------------------------
        expression_infos            Optional list of PopupExpressionInfo objects. List of Arcade expressions added to the pop-up.
        ---------------------       -------------------------------------------------------------------
        field_infos                 Optional list of FieldInfo objects. Array of fieldInfo information properties.
                                    This information is provided by the service layer definition.
                                    When the description uses name/value pairs, the order of the array
                                    is how the fields display in the editable Map Viewer popup and the
                                    resulting popup. It is also possible to specify HTML-formatted content.
        ---------------------       -------------------------------------------------------------------
        layer_options               Optional LayerOptions class.
        ---------------------       -------------------------------------------------------------------
        media_infos                 Optional list of MediaInfo objects. Array of various mediaInfo to display.
        ---------------------       -------------------------------------------------------------------
        popup_elements              Optional list of PopupElement objects. An array of popupElement objects
                                    that represent an ordered list of popup elements.
        ---------------------       -------------------------------------------------------------------
        show_attachments            Optional bool. Indicates whether attachments will be loaded for
                                    feature layers that have attachments.
        =====================       ===================================================================
        """
        # Check if popup exists
        if self._layer.popup_info is None:
            # create empty popup info
            self._layer.popup_info = PopupInfo()

        # Add any edits made to the popup
        if title is not None:
            self._layer.popup_info.title = title
        if description is not None:
            self._layer.popup_info.description = description

        if expression_infos is not None:
            validated_expressions = []
            for expression in expression_infos:
                # validate in the widget's spec class
                # this is necessary to normalize the class names since we changed some names above
                validated_expressions.append(
                    self._spec.ExpressionInfo(**expression.dict())
                )
            self._layer.popup_info.expression_infos = validated_expressions

        if field_infos is not None:
            validated_field_infos = []
            for field_info in field_infos:
                # validate in the widget's spec class
                # this is necessary to normalize the class names since we changed some names above
                validated_field_infos.append(self._spec.FieldInfo(**field_info.dict()))
            self._layer.popup_info.field_infos = validated_field_infos

        if layer_options is not None:
            layer_options = self._spec.LayerOptions(**layer_options.dict())
            self._layer.popup_info.layer_options = layer_options

        if media_infos is not None:
            validated_media_infos = []
            for media_info in media_infos:
                # validate in the widget's spec class
                # this is necessary to normalize the class names since we changed some names above
                validated_media_infos.append(self._spec.MediaInfo(**media_info.dict()))
            self._layer.popup_info.media_infos = validated_media_infos

        if popup_elements is not None:
            validated_popup_elements = []
            # there are various popup elements that can be added
            # validate each one in the widget's spec class
            for popup_element in popup_elements:
                if popup_element.type == "attachments":
                    validated_popup_elements.append(
                        self._spec.PopupElementAttachments(**popup_element.dict())
                    )
                elif popup_element.type == "expression":
                    validated_popup_elements.append(
                        self._spec.PopupElementExpression(**popup_element.dict())
                    )
                elif popup_element.type == "fields":
                    validated_popup_elements.append(
                        self._spec.PopupElementFields(**popup_element.dict())
                    )
                elif popup_element.type == "media":
                    validated_popup_elements.append(
                        self._spec.PopupElementMedia(**popup_element.dict())
                    )
                elif popup_element.type == "relationship":
                    validated_popup_elements.append(
                        self._spec.PopupElementRelationship(**popup_element.dict())
                    )
                elif popup_element.type == "text":
                    validated_popup_elements.append(
                        self._spec.PopupElementText(**popup_element.dict())
                    )
                else:
                    raise ValueError(
                        f"Invalid popup element type: {popup_element.type}"
                    )

            self._layer.popup_info.popup_elements = validated_popup_elements

        if show_attachments is not None:
            self._layer.popup_info.show_attachments = show_attachments

        self._source._update_source()

        return True
